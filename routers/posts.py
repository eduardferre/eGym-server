import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ddbb.mongodb.client import mongodb_client
from ddbb.mongodb.models.post import Post
from ddbb.mongodb.schemas.post import posts_schema, post_schema
from ddbb.mongodb.schemas.user import user_schema


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
    post = await search_post("_id", ObjectId(id))

    if post == None:
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
    user = await mongodb_client.users.find_one({"username": post.creator})
    if user == None:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    logging.info(f"The post is being processed")

    post_dic = dict(post)
    del post_dic["id"]

    result = await mongodb_client.posts.insert_one(post_dic)
    id = result.inserted_id

    logging.info(f"The post {ObjectId(id)} has been inserted correctly in the database")
    new_post = await mongodb_client.posts.find_one({"_id": ObjectId(id)})
    return Post(**post_schema(new_post))


@router.put("/", response_model=Post, status_code=status.HTTP_200_OK)
async def updatePost(post: Post):
    logging.info("PUT /posts/")
    post_search = await search_post("_id", ObjectId(post.id))

    if type(post_search) != Post:
        logging.info(f"The post with id = '{post.id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id = '{post.id}' does not exist",
        )

    user = await mongodb_client.users.find_one({"username": post.creator})
    if user == None:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    post_dic = dict(post)
    del post_dic["id"]

    try:
        await mongodb_client.posts.find_one_and_replace(
            {"_id": ObjectId(post.id)}, post_dic
        )
        logging.info(f"The post with id = {post.id} has been updated")
    except:
        logging.info(f"The post with id = {post.id} has not been updated")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The post with id = {post.id} has not been updated",
        )
    return await search_post("_id", ObjectId(post.id))


@router.delete("/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def deletePost(id: str):
    logging.info(f"DELETE /posts/{id}")
    post_search = await search_post("_id", ObjectId(id))

    if type(post_search) != Post:
        logging.info(f"The post with id = '{id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id = '{id}' does not exist",
        )

    try:
        await mongodb_client.posts.find_one_and_delete({"_id": ObjectId(id)})
        logging.info(f"The post with id = {id} has been deleted")
    except:
        logging.info(f"The post with id = {id} has not been deleted")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The post with id = {id} has not been deleted",
        )
    return post_search


@router.delete(
    "/creatorPosts/{creator}", response_model=list[Post], status_code=status.HTTP_200_OK
)
async def deleteAllCreatorPosts(creator: str):
    logging.info(f"DELETE /posts/creatorPosts/{creator}")
    user = await mongodb_client.users.find_one({"username": creator})

    if user == None:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    result = await search_posts("creator", creator)

    if len(result) == 0:
        logging.info(f"The user {creator} has no posts, so, anything will be deleted")
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {creator} has no posts, so, anything will be deleted",
        )

    post_search = posts_schema(result)
    posts_list = list()
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