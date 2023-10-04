import sys
import os

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest

from bson import ObjectId
from utils.logger import logging
from fastapi import APIRouter, HTTPException, status

from db.mongodb.models.comment import Comment
from db.mongodb.models.post import Post
from src.main.routers import comments, posts

id_test_404 = "507f1f77bcf86cd799439011"
comment_add = Comment(
    **{"id": "string", "postId": "string", "creator": "string", "content": "string"}
)


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getComments_NoContent():
    with pytest.raises(HTTPException) as exception:
        await comments.getComments()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getCommentById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await comments.getCommentById("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getCommentById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await comments.getCommentById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getCommentsByCreator_NotFound():
    with pytest.raises(HTTPException) as exception:
        await comments.getCommentsByCreator("user_not_found")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getCommentsByCreator_NoContent():
    comments_list = await comments.getCommentsByCreator("eduardferre")
    assert len(comments_list) == 0


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getPostComments_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await comments.getPostComments("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getPostComments_NotFound():
    with pytest.raises(HTTPException) as exception:
        await comments.getPostComments(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_getPostComments_NoContent():
    global post_response
    post_response = await posts.getPostsByCreator("eduardferre")
    with pytest.raises(HTTPException) as exception:
        await comments.getPostComments(post_response[0]["id"])
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_addCommentToPost_PostIdBadRequest():
    with pytest.raises(HTTPException) as exception:
        await comments.addCommentToPost("is_not_valid_id", comment_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400

    comment_add.postId = "is_not_valid_id"
    with pytest.raises(HTTPException) as exception:
        await comments.addCommentToPost("is_not_valid_id", comment_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_addCommentToPost_PostNotFound():
    comment_add.postId = id_test_404
    with pytest.raises(HTTPException) as exception:
        await comments.addCommentToPost(id_test_404, comment_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_addCommentToPost_UserNotFound():
    comment_add.postId = post_response[0]["id"]
    comment_add.creator = "user_is_not_found"
    with pytest.raises(HTTPException) as exception:
        await comments.addCommentToPost(post_response[0]["id"], comment_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_addCommentToPost_Ok():
    comment_add.postId = post_response[0]["id"]
    comment_add.creator = post_response[0]["creator"]
    comment_response = await comments.addCommentToPost(comment_add.postId, comment_add)
    assert isinstance(comment_response, Comment)
    assert comment_response.postId == comment_add.postId
    assert comment_response.creator == comment_add.creator
    assert comment_response.content == comment_add.content
    comment_add.id = comment_response.id

    global comment_duplicated
    comment_duplicated = await comments.addCommentToPost(
        comment_add.postId, comment_add
    )


@pytest.mark.order(after="posts_test.py::test_addPost_Created")
@pytest.mark.asyncio
async def test_deleteCommentFromPost_Ok():
    comment_response = await comments.deleteCommentFromPost(
        comment_add.postId, comment_add.id
    )
    assert isinstance(comment_response, Comment)
    assert comment_response.id == comment_add.id
    assert comment_response.postId == comment_add.postId
    assert comment_response.creator == comment_add.creator
    assert comment_response.content == comment_add.content

    post_comments = await comments.getPostComments(comment_add.postId)
    for comment in post_comments:
        comment = comment
        assert comment.id != comment_add.id

    await comments.deleteCommentFromPost(
        comment_duplicated.postId, comment_duplicated.id
    )  #!THIS SHOULD BE REMOVED - IT IS ONLY TO SEE HOW TESTS PASS AS NORMAL
