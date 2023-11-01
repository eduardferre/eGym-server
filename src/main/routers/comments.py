import src.main.services.auth as auth_handler_class

from utils.logger import logging

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from typing import Optional

from db.mongodb.client import mongodb_client
from db.mongodb.models.comment import Comment
from db.mongodb.models.post import Post
from db.mongodb.models.user import User
from db.mongodb.schemas.comment import comments_schema, comment_schema
import src.main.routers.posts as posts
import src.main.routers.users as users

oauth2_scheme = OAuth2PasswordBearer("/transactions/login")
auth_handler = auth_handler_class.Auth()


def token_validation(token: str):
    return auth_handler.decode_token(token)


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[Comment], status_code=status.HTTP_200_OK)
async def getComments(token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info("GET /comments/")
        comments_list = await search_comments(None, None)

        if len(comments_list) == 0:
            logging.info("There are no comments in the database")
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="There are no comments in the database",
            )
        return comments_schema(comments_list)


@router.get("/{id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def getCommentById(id: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"GET /comments/{id}")
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        comment = await search_comment("_id", ObjectId(id))

        if type(comment) != Comment:
            logging.info(f"The comment with id = {id} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The comment with id = {id} does not exist",
            )
        return await search_comment("_id", ObjectId(id))


@router.get(
    "/creator/{creator}", response_model=list[Comment], status_code=status.HTTP_200_OK
)
async def getCommentsByCreator(creator: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"GET /comments/creator/{creator}")
        await users.getUserByUsername(creator, token)

        # if type(user_search) != User:
        #     logging.info(f"The user specified does not exist in the database")
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"The user specified does not exist in the database",
        #     )

        comments_list = await search_comments("creator", creator)

        if len(comments_list) == 0:
            logging.info("There are no comments in the database made by this user")
            # raise HTTPException(
            #     status_code=status.HTTP_204_NO_CONTENT,
            #     detail="There are no comments in the database made by this user",
            # )
        return comments_schema(comments_list)


@router.get(
    "/post/{postId}", response_model=list[Comment], status_code=status.HTTP_200_OK
)
async def getPostComments(postId: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"GET /post/{postId}")
        if not ObjectId.is_valid(postId):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        post = await posts.getPostById(postId, token)

        # if type(post) != Post:
        #     logging.info(f"The post with id = {id} does not exist")
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"The post with id = {id} does not exist",
        #     )

        if len(post.comments) == 0:
            logging.info(f"There are no comments for post {post.id}")
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"There are no comments for post {post.id}",
            )

        return post.comments


@router.post(
    "/post/{postId}", response_model=Comment, status_code=status.HTTP_201_CREATED
)
async def addCommentToPost(
    postId: str, comment: Comment, token: str = Depends(oauth2_scheme)
):
    if token_validation(token) != None:
        logging.info("POST /comments/post/{postId}")
        if not ObjectId.is_valid(postId) or postId != comment.postId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        search_post = await posts.getPostById(postId, token)

        # if type(search_post) != Post:
        #     logging.info(f"The post with id = {postId} does not exist")
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"The post with id = {postId} does not exist",
        #     )

        search_user = await users.getUserByUsername(comment.creator, token)

        # if type(search_user) != User:
        #     logging.info(f"The user '{comment.creator}' does not exist")
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"The user '{comment.creator}' does not exist",
        #     )

        logging.info(f"Comment is being added to 'comments' collection")

        comment_dic = dict(comment)
        comment_dic["postId"] = postId
        post_comment = comment_dic.copy()
        del comment_dic["id"]

        try:
            result = await mongodb_client.comments.insert_one(comment_dic)
            id = result.inserted_id
            post_comment["id"] = str(id)

            logging.info(
                f"The comment '{ObjectId(id)}' has been inserted correctly in the database"
            )
        except:
            logging.info(f"The comment has not been uploaded")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The comment has not been uploaded",
            )

        try:
            search_post.comments.append(post_comment)
            await posts.updatePost(search_post, token)
            logging.info(f"Comment '{ObjectId(id)}' has been posted in post '{postId}'")
        except:
            await deleteCommentFromPost(postId, ObjectId(id), token)
            logging.info(f"The comment '{ObjectId(id)}' has not been uploaded")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The comment '{ObjectId(id)}' has not been uploaded",
            )

        new_comment = await mongodb_client.comments.find_one({"_id": ObjectId(id)})
        return Comment(**comment_schema(new_comment))


@router.put(
    "/post/{postId}", response_model=Comment, status_code=status.HTTP_201_CREATED
)
async def updateCommentFromPost(
    postId: str, comment: Comment, token: str = Depends(oauth2_scheme)
):
    if token_validation(token) != None:
        logging.info("PUT /comments/post/{postId}")
        if (
            not ObjectId.is_valid(comment.id)
            or not ObjectId.is_valid(postId)
            or postId != comment.postId
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        comment_search = await search_comment("_id", ObjectId(comment.id))
        if type(comment_search) != Comment:
            logging.info(f"The comment with id = '{comment.id}' does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The comment with id = '{comment.id}' does not exist",
            )

        post = await posts.search_post("_id", ObjectId(comment.postId))
        if type(post) != Post:
            logging.info(f"The post specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The post specified does not exist in the database",
            )

        user = await users.search_user("username", comment.creator)
        if type(user) != User:
            logging.info(f"The user specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user specified does not exist in the database",
            )

        logging.info(f"Comment is being updated to 'comments' collection")

        comment_dic = dict(comment)
        del comment_dic["id"]
        post_comment = comment_dic.copy()

        try:
            await mongodb_client.comments.find_one_and_replace(
                {"_id": ObjectId(comment.id)}, comment_dic
            )
            logging.info(f"The comment with id = '{comment.id}' has been updated")
        except:
            logging.info(f"The comment with id = '{comment.id}' has not been updated")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The comment with id = '{comment.id}' has not been updated",
            )

        logging.info(f"Comment is being updated to post {postId}")
        try:
            search_post = await posts.getPostById(postId, token)

            for index, single_comment in enumerate(search_post.comments):
                if single_comment.id == comment.id:
                    search_post.comments[index].content = comment.content
                    break

            post = await posts.updatePost(search_post, token)
            logging.info(f"Comment has been updated in post '{post.id}'")
        except:
            await mongodb_client.comments.find_one_and_replace(
                {"_id": ObjectId(comment.id)}, post_comment
            )
            logging.info(f"The comment '{comment.id}' has not been updated")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The '{comment.id}' comment has not been updated",
            )

        return await search_comment("_id", ObjectId(comment.id))


@router.delete(
    "/post/{postId}/comment/{commentId}",
    response_model=Comment,
    status_code=status.HTTP_200_OK,
)
async def deleteCommentFromPost(
    postId: str, commentId: str, token: str = Depends(oauth2_scheme)
):
    if token_validation(token) != None:
        logging.info(f"DELETE /comments/post/{postId}/comment/{commentId}")
        if not ObjectId.is_valid(commentId) or not ObjectId.is_valid(postId):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        comment_search = await search_comment("_id", ObjectId(commentId))
        if type(comment_search) != Comment:
            logging.info(f"The comment with id = '{commentId}' does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The comment with id = '{commentId}' does not exist",
            )
        if comment_search.postId != postId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This comment does not belong to the specified post",
            )

        post_search = await posts.search_post("_id", ObjectId(postId))
        if type(post_search) != Post:
            logging.info(f"The post with id = '{postId}' does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The post with id = '{postId}' does not exist",
            )

        try:
            await mongodb_client.comments.find_one_and_delete(
                {"_id": ObjectId(commentId)}
            )
            logging.info(f"The comment with id = {commentId} has been deleted")
        except:
            logging.info(f"The comment with id = {commentId} has not been deleted")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The comment with id = {commentId} has not been deleted",
            )

        logging.info(f"Comment is being deleted from post {postId}")
        try:
            search_post = await posts.getPostById(postId, token)

            for index, single_comment in enumerate(search_post.comments):
                if single_comment.id == commentId:
                    search_post.comments.pop(index)
                    break

            post = await posts.updatePost(search_post, token)
            logging.info(f"Comment has been deleted from post '{post.id}'")
        except:
            comment_dic = dict(comment_search)
            del comment_dic["id"]
            comment_dic["_id"] = ObjectId(comment_search.id)
            result = await mongodb_client.comments.insert_one(comment_dic)
            logging.info(
                f"The comment '{ObjectId(result.inserted_id)}' has not been deleted"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The '{ObjectId(result.inserted_id)}' comment has not been deleted",
            )

        return comment_search


@router.delete(
    "/postComments/{postId}",
    response_model=list[Comment],
    status_code=status.HTTP_200_OK,
)
async def deleteAllPostComments(postId: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"DELETE /comments/postComments/{postId}")
        if not ObjectId.is_valid(postId):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        post = await posts.search_post("_id", ObjectId(postId))

        if type(post) != Post:
            logging.info(f"The post specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The post specified does not exist in the database",
            )

        post_comments = post.comments.copy()
        if len(post_comments) == 0:
            logging.info(f"There are no comments in post '{post.id}")
            # raise HTTPException(
            #     status_code=status.HTTP_204_NOT_FOUND,
            #     detail=f"There are no comments in post '{post.id}",
            # )
        else:
            list_comments_id = list()
            try:
                for comment in post_comments:
                    list_comments_id.append(ObjectId(comment.id))

                query = {"_id": {"$in": list_comments_id}}

                await mongodb_client.comments.delete_many(query)
                post.comments.clear()
                await posts.updatePost(post, token)
                logging.info(f"All the comments of post {post.id} have been deleted")
            except:
                logging.info(
                    f"The comments of post '{post.id}' could not be deleted due to an issue"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"The comments of post '{post.id}' could not be deleted due to an issue",
                )

        return post_comments


# Methods
async def search_comment(field: str, key):
    try:
        comment = await mongodb_client.comments.find_one({field: key})
        logging.info(f"The comment with {field} = {key} exists in the database")
        return Comment(**comment_schema(comment))
    except:
        return {"error": f"There's not any comment with {field} -> {key}"}


async def search_comments(field: Optional[str], key: Optional[any]):
    comments_list = list()
    if (field and key) == None:
        async for comment in mongodb_client.comments.find():
            comments_list.append(comment)
            logging.info(
                f"({len(comments_list)}) -> {comment['_id']} - {comment['creator']}"
            )
    else:
        async for comment in mongodb_client.comments.find({field: key}):
            comments_list.append(comment)
            logging.info(
                f"({len(comments_list)}) -> {comment['_id']} - {comment['creator']}"
            )

    logging.info(
        f"The number of comments found in the database is {len(comments_list)}"
    )
    return comments_list
