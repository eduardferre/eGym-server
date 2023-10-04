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

from db.mongodb.models.post import Post
from src.main.routers import posts, users


id_test_404 = "507f1f77bcf86cd799439011"
post_add = Post(
    **{
        "id": "string",
        "creator": "eduardferre",
        "url": "string",
        "caption": "string",
        "likes": 0,
        "comments": [],
    }
)


@pytest.mark.asyncio
async def test_getPosts_NoContent():
    with pytest.raises(HTTPException) as exception:
        await posts.getPosts()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_getPostById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await posts.getPostById("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_getPostById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await posts.getPostById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_getPostByCreator_NotFound():
    with pytest.raises(HTTPException) as exception:
        await posts.getPostsByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getPostByCreator_NoContent():
    with pytest.raises(HTTPException) as exception:
        await posts.getPostsByCreator("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_addPost_NotFound():
    post_add.creator = "not_found"
    with pytest.raises(HTTPException) as exception:
        await posts.addPost(post_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_addPost_Created():
    post_add.creator = "eduardferre"
    post_response = await posts.addPost(post_add)
    global id_test_Ok
    id_test_Ok = post_response.id
    assert isinstance(post_response, Post)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getPosts_Ok():
    posts_list = await posts.getPosts()
    assert isinstance(posts_list, list)
    assert len(posts_list) > 0


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getPostById_Ok():
    post_response = await posts.getPostById(id_test_Ok)
    assert isinstance(post_response, Post)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_getPostByCreator_Ok():
    posts_list = await posts.getPostsByCreator("eduardferre")
    for post in posts_list:
        posts_list[posts_list.index(post)] = Post(**post)
    assert isinstance(posts_list, list)
    assert len(posts_list) > 0

    user_update = await users.getUserByUsername("eduardferre")
    assert user_update.postsLog == posts_list
    user_update.username = "eduardferr"
    user_response = await users.updateUser(user_update)
    assert user_response.postsLog[0].creator == user_update.username

    user_update.username = "eduardferre"
    await users.updateUser(user_update)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updatePost_BadRequest():
    post_add.id = "id_is_not_valid"
    with pytest.raises(HTTPException) as exception:
        await posts.updatePost(post_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updatePost_NotFound():
    post_add.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await posts.updatePost(post_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updatePost_NoContent():
    post_add.creator = "eduardferre"
    post_add.id = id_test_Ok
    with pytest.raises(HTTPException) as exception:
        await posts.updatePost(post_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updatePost_User_NotFound():
    post_add.id = id_test_Ok
    post_add.creator = "not_found"
    with pytest.raises(HTTPException) as exception:
        await posts.updatePost(post_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_updatePost_Created():
    post_add.creator = "eduardferre"
    post_add.id = id_test_Ok
    post_add.caption = "new_caption"
    post_response = await posts.updatePost(post_add)
    assert isinstance(post_response, Post)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deletePost_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await posts.deletePost("id_is_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deletePost_NotFound():
    with pytest.raises(HTTPException) as exception:
        await posts.deletePost(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deletePost_Ok():
    post_response = await posts.deletePost(id_test_Ok)
    assert isinstance(post_response, Post)


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteAllCreatorPosts_NotFound():
    post_add.creator = "eduardferre"
    post_response = await posts.addPost(post_add)
    assert isinstance(post_response, Post)

    with pytest.raises(HTTPException) as exception:
        await posts.deleteAllCreatorPosts("not_found")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(after="users_test.py::test_addUser_Created")
@pytest.mark.asyncio
async def test_deleteAllCreatorPosts_Ok():
    posts_list = await posts.deleteAllCreatorPosts("eduardferre")
    assert isinstance(posts_list, list)
    assert len(posts_list) > 0

    posts_list = await posts.deleteAllCreatorPosts("eduardferre")
    assert isinstance(posts_list, list)
    assert len(posts_list) == 0
