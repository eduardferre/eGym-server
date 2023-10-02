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

from src.main.routers import comments, posts

id_test_404 = "507f1f77bcf86cd799439011"


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
    post_response = await posts.getPostsByCreator("eduardferre")
    with pytest.raises(HTTPException) as exception:
        await comments.getPostComments(post_response[0].id)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204
