from utils.logger import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from db.mongodb.client import mongodb_client
from db.mongodb.models.post import Post
from db.mongodb.schemas.post import posts_schema, post_schema
from db.mongodb.models.user import User
import src.main.routers.users as users
import src.main.routers.comments as comments


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[Post], status_code=status.HTTP_200_OK)
async def getPosts():
    logging.info("GET /posts/")
    posts_list = await search_posts(None, None)

    if len(posts_list) == 0:
        logging.info("There are no posts in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no posts in the database",
        )
    return posts_schema(posts_list)


@router.get("/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def getPostById(id: str):
    logging.info(f"GET /posts/{id}")
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    post = await search_post("_id", ObjectId(id))
    if type(post) != Post:
        logging.info(f"The post with id = {id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id = {id} does not exist",
        )
    return await search_post("_id", ObjectId(id))


@router.get(
    "/creator/{creator}", response_model=list[Post], status_code=status.HTTP_200_OK
)
async def getPostsByCreator(creator: str):
    logging.info(f"GET /posts/creator/{creator}")
    user = await users.search_user("username", creator)

    if type(user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    posts_list = await search_posts("creator", creator)

    if len(posts_list) == 0:
        logging.info("There are no posts in the database made by this user")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no posts in the database made by this user",
        )
    return posts_schema(posts_list)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def addPost(post: Post):
    logging.info("POST /posts/")
    search_user = await users.search_user("username", post.creator)
    if type(search_user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    logging.info(f"The post is being processed")

    post_dic = dict(post)
    user_post = post_dic.copy()
    del post_dic["id"]

    try:
        result = await mongodb_client.posts.insert_one(post_dic)
        id = result.inserted_id
        user_post["id"] = str(id)

        logging.info(
            f"The post {ObjectId(id)} has been inserted correctly in the database"
        )
    except:
        logging.info("The post has not been uploaded")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The post has not been uploaded",
        )

    try:
        search_user.postsLog.append(user_post)
        await users.updateUser(search_user)
        logging.info(
            f"Post '{ObjectId(id)}' has been posted in user '{search_user.id}'"
        )
    except:
        await deletePost(ObjectId(id))
        logging.info(f"The post '{ObjectId(id)}' has not been uploaded")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The post '{ObjectId(id)}' has not been uploaded",
        )

    new_post = await mongodb_client.posts.find_one({"_id": ObjectId(id)})
    return Post(**post_schema(new_post))


@router.put("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def updatePost(post: Post):
    logging.info("PUT /posts/")
    if not ObjectId.is_valid(post.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    post_search = await search_post("_id", ObjectId(post.id))
    if type(post_search) != Post:
        logging.info(f"The post with id = '{post.id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id = '{post.id}' does not exist",
        )

    if post.__eq__(post_search):
        logging.info(f"The post '{post.id}' has not been changed so no update required")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The post '{post.id}' has not been changed so no update required",
        )

    search_user = await users.search_user("username", post.creator)
    if type(search_user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    logging.info("The post is being processed")

    dict_comments = list()
    for comment in post.comments:
        dict_comments.append(dict(comment))
    post.comments.clear()
    post.comments = dict_comments

    post_dic = dict(post)
    del post_dic["id"]

    try:
        user_search = await users.getUserByUsername(post_search.creator)

        await mongodb_client.posts.find_one_and_replace(
            {"_id": ObjectId(post.id)}, post_dic
        )
        logging.info(f"The post with id = {post.id} has been updated")
    except Exception as e:
        print(e)
        logging.info(f"The post with id = {post.id} has not been updated")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The post with id = {post.id} has not been updated",
        )
    else:
        for post_for in search_user.postsLog:
            if post.id == post_for.id:
                index = search_user.postsLog.index(post_for)
                search_user.postsLog.insert(index, post)
                search_user.postsLog.remove(post_for)

        await users.updateUser(search_user)
        logging.info(f"Post logs of '{search_user.username}' has been updated")
    return await search_post("_id", ObjectId(post.id))


@router.delete("/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def deletePost(id: str):
    logging.info(f"DELETE /posts/{id}")
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    post_search = await search_post("_id", ObjectId(id))

    if type(post_search) != Post:
        logging.info(f"The post with id = '{id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id = '{id}' does not exist",
        )

    try:
        search_user = await users.getUserByUsername(post_search.creator)

        logging.info(f"Deleting post comments")
        await comments.deleteAllPostComments(id)

        await mongodb_client.posts.find_one_and_delete({"_id": ObjectId(id)})
        logging.info(f"The post with id = {id} has been deleted")
    except:
        for comment in post_search.comments:
            comment_dict = dict(comment)
            await mongodb_client.comments.insert_one(comment_dict)
        logging.info("Comments have not been deleted")

        logging.info(f"The post with id = {id} has not been deleted")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The post with id = {id} has not been deleted",
        )
    else:
        for post_for in search_user.postsLog:
            if post_search.id == post_for.id:
                search_user.postsLog.remove(post_for)

        await users.updateUser(search_user)
        logging.info(f"Post logs of '{search_user.username}' has been updated")
    return post_search


@router.delete(
    "/creatorPosts/{creator}", response_model=list[Post], status_code=status.HTTP_200_OK
)
async def deleteAllCreatorPosts(creator: str):
    logging.info(f"DELETE /posts/creatorPosts/{creator}")
    user = await users.search_user("username", creator)

    if type(user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    result = await search_posts("creator", creator)
    posts_list = list()

    if len(result) == 0:
        logging.info(f"The user {creator} has no posts, so, anything will be deleted")
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail=f"The user {creator} has no posts, so, anything will be deleted",
        # )
    else:
        logging.info(f"The '{creator}' posts will be deleted")
        post_search = posts_schema(result)
        for post in post_search:
            posts_list.append(await deletePost(post["id"]))

    return posts_list


# Methods
async def search_post(field: str, key):
    try:
        post = await mongodb_client.posts.find_one({field: key})
        logging.info(f"The post with {field} = {key} exists in the database")
        return Post(**post_schema(post))
    except:
        return {"error": f"There's not any post with {field} -> {key}"}


async def search_posts(field: Optional[str], key: Optional[any]):
    posts_list = list()
    if (field and key) == None:
        async for post in mongodb_client.posts.find():
            posts_list.append(post)
            logging.info(
                f"({len(posts_list)}) -> {post['_id']} - {post['creator']} - {post['likes']}"
            )
    else:
        async for post in mongodb_client.posts.find({field: key}):
            posts_list.append(post)
            logging.info(
                f"({len(posts_list)}) -> {post['_id']} - {post['creator']} - {post['likes']}"
            )

    logging.info(f"The number of posts found in the database is {len(posts_list)}")
    return posts_list
