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

from db.mongodb.models.user import User
from src.main.routers import users

id_test_404 = "507f1f77bcf86cd799439011"
user_add = User(
    **{
        "id": "507f1f77bcf86cd799439011",
        "username": "eduardferre",
        "fullname": "Eduard Ferré Sánchez",
        "email": "eduardferresanchez@gmail.com",
        "phone": "616127758",
        "age": 23,
        "height": 176,
        "weight": 100,
        "physicalActivity": 2.0,
        "role": "Powerlifter",
        "followers": 250,
        "postsLog": [],
        "routinesLog": [],
        "routines": [],
        "profilePicture": "https://blablabla",
        "backgroundPicture": "https://blablabla",
    }
)
user_update_conflict = User(
    **{
        "id": "507f1f77bcf86cd799439011",
        "username": "aleixferre",
        "fullname": "Eduard Ferré Sánchez",
        "email": "eduardferresanchez@gmail.com",
        "phone": "616127758",
        "age": 23,
        "height": 176,
        "weight": 100,
        "physicalActivity": 2.0,
        "role": "Powerlifter",
        "followers": 250,
        "postsLog": [],
        "routinesLog": [],
        "routines": [],
        "profilePicture": "https://blablabla",
        "backgroundPicture": "https://blablabla",
    }
)


# @pytest.mark.order(1)
@pytest.mark.asyncio
async def test_addUser_Created():
    user_response = await users.addUser(user=user_add)
    await users.addUser(user=user_update_conflict)
    global id_test_Ok
    id_test_Ok = user_response.id
    assert isinstance(user_response, User)


# @pytest.mark.order(3)
@pytest.mark.asyncio
async def test_getUsers_Ok():
    users_list = await users.getUsers()
    assert isinstance(users_list, list)
    assert len(users_list) > 0


# @pytest.mark.order(1)
@pytest.mark.asyncio
async def test_addUser_Conflict():
    with pytest.raises(HTTPException) as exception:
        await users.addUser(user=user_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.asyncio
async def test_getUserById_Ok():
    user_response = await users.getUserById(id_test_Ok)
    assert isinstance(user_response, User)


@pytest.mark.asyncio
async def test_getUserById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await users.getUserById("id_test_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_getUserById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await users.getUserById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_getUserByUsername_Ok():
    user_search = await users.getUserByUsername("eduardferre")
    assert isinstance(user_search, User)


@pytest.mark.asyncio
async def test_updateUser_NoContent():
    user_add.id = id_test_Ok
    user_add.username = "eduardferre"
    with pytest.raises(HTTPException) as exception:
        await users.updateUser(user_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_updateUser_Ok():
    user_add.username = "eduardfer"
    user_add.id = id_test_Ok
    user_response = await users.updateUser(user_add)
    assert isinstance(user_response, User)
    assert user_response == user_add


@pytest.mark.asyncio
async def test_getUserByUsername_NotFound():
    with pytest.raises(HTTPException) as exception:
        await users.getUserByUsername("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_updateUser_BadRequest():
    user_add.id = "id_test_not_valid"
    with pytest.raises(HTTPException) as exception:
        await users.updateUser(user_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_updateUser_NotFound():
    user_add.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await users.updateUser(user_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_updateUser_Conflict():
    user_add.username = "aleixferre"
    user_add.id = id_test_Ok
    with pytest.raises(HTTPException) as exception:
        await users.updateUser(user_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.asyncio
async def test_deleteUser_Ok():
    user_search = await users.getUserByUsername("eduardfer")
    assert isinstance(user_search, User)
    user_response = await users.deleteUser(user_search.id)
    assert isinstance(user_response, User)
    assert user_response == user_search


@pytest.mark.asyncio
async def test_deleteUser_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await users.deleteUser("id_test_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_deleteUser_NotFound():
    with pytest.raises(HTTPException) as exception:
        await users.deleteUser(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.order(before="test_getUsers_NoContent")
@pytest.mark.asyncio
async def test_deleteAllUsers_Ok():
    user_response = await users.deleteAllUsers()
    assert isinstance(user_response, list)


@pytest.mark.order("last")
@pytest.mark.asyncio
async def test_getUsers_NoContent():
    with pytest.raises(HTTPException) as exception:
        await users.getUsers()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204
