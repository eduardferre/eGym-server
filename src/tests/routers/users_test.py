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
        "followers": [],
        "following": [],
        "postsLog": [],
        "routinesLog": [],
        "routines": [],
        "profilePicture": "https://blablabla",
        "backgroundPicture": "https://blablabla",
        "public": False,
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
        "followers": [],
        "following": [],
        "postsLog": [],
        "routinesLog": [],
        "routines": [],
        "profilePicture": "https://blablabla",
        "backgroundPicture": "https://blablabla",
        "public": True,
    }
)


@pytest.mark.asyncio
async def test_addUser_Created():
    user_response = await users.addUser(user=user_add)
    await users.addUser(user=user_update_conflict)
    global id_test_Ok
    id_test_Ok = user_response.id
    user_add.id = id_test_Ok
    assert isinstance(user_response, User)


@pytest.mark.asyncio
async def test_getPublicUsers_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await users.getPublicUsers("attribute_not_valid", "any")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_getPublicUsers_All_Ok():
    user_list = await users.getPublicUsers("public", "users")
    assert user_list[0].role == ""
    assert user_list[0].age == 0
    assert len(user_list[0].routines) == 0
    assert len(user_list[0].postsLog) == len(user_add.postsLog)

    assert user_list[1].role == user_update_conflict.role
    assert user_list[1].age == user_update_conflict.age
    assert user_list[1].routines == user_update_conflict.routines


@pytest.mark.asyncio
async def test_getPublicUsers_ById_Ok():
    user_list = await users.getPublicUsers("_id", user_add.id)
    logging.critical(user_list)
    assert user_list[0].role == ""
    assert user_list[0].age == 0
    assert len(user_list[0].routines) == 0
    assert len(user_list[0].postsLog) == len(user_add.postsLog)


@pytest.mark.asyncio
async def test_getPublicUsers_ByUsername_Ok():
    user_list = await users.getPublicUsers("username", "eduardferre")
    assert user_list[0].role == ""
    assert user_list[0].age == 0
    assert len(user_list[0].routines) == 0
    assert len(user_list[0].postsLog) == len(user_add.postsLog)


@pytest.mark.asyncio
async def test_followUser_Ok():
    user_add.following = await users.followUser(
        user_add.username, user_update_conflict.username
    )
    user_followed = await users.getUserByUsername(user_update_conflict.username)

    assert user_followed.username in user_add.following
    assert user_add.username in user_followed.followers


@pytest.mark.asyncio
async def test_followUser_NoContent():
    with pytest.raises(HTTPException) as exception:
        await users.followUser(user_add.username, user_update_conflict.username)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_unfollowUser_Ok():
    user_add.following = await users.unfollowUser(
        user_add.username, user_update_conflict.username
    )
    user_unfollowed = await users.getUserByUsername(user_update_conflict.username)

    assert not user_unfollowed.username in user_add.following
    assert not user_add.username in user_unfollowed.followers


@pytest.mark.asyncio
async def test_unfollowUser_NoContent():
    with pytest.raises(HTTPException) as exception:
        await users.unfollowUser(user_add.username, user_update_conflict.username)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_getUsers_Ok():
    users_list = await users.getUsers()
    assert isinstance(users_list, list)
    assert len(users_list) > 0


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
