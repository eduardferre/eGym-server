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


# @pytest.mark.asyncio
# async def test_addUser_Created():
#     user = {
#         "id": "507f1f77bcf86cd799439011",
#         "username": "eduardferre",
#         "fullname": "Eduard Ferré Sánchez",
#         "email": "eduardferresanchez@gmail.com",
#         "phone": "616127758",
#         "age": 23,
#         "height": 176,
#         "weight": 100,
#         "physicalActivity": 2.0,
#         "role": "Powerlifter",
#         "followers": 250,
#         "postsLog": [],
#         "routinesLog": [],
#         "routines": [],
#         "profilePicture": "https://blablabla",
#         "backgroundPicture": "https://blablabla",
#     }

#     response = await users.addUser(user=user)


@pytest.mark.asyncio
async def test_deleteUser_Ok():
    list_users = await users.getUsers()
    response = await users.deleteUser(User(**list_users[0]).id)
    assert type(response) == list()


@pytest.mark.asyncio
async def test_getUsers_NoContents():
    response = await users.getUsers()
    logging.info(response)
    assert response != None


# @pytest.mark.asyncio
# async def test_getUsers_NoContent():
#     with pytest.raises(HTTPException) as exception:
#         await users.getUsers()
#     assert isinstance(exception.value, HTTPException)
#     assert exception.value.status_code == 204
#     assert exception.value.detail == "There are no users in the database"


# @pytest.mark.asyncio
# async def test_addUser_Conflict():
#     user = {
#         "id": "507f1f77bcf86cd799439011",
#         "username": "eduardferre",
#         "fullname": "Eduard Ferré Sánchez",
#         "email": "eduardferresanchez@gmail.com",
#         "phone": "616127758",
#         "age": 23,
#         "height": 176,
#         "weight": 100,
#         "physicalActivity": 2.0,
#         "role": "Powerlifter",
#         "followers": 250,
#         "postsLog": [],
#         "routinesLog": [],
#         "routines": [],
#         "profilePicture": "https://blablabla",
#         "backgroundPicture": "https://blablabla",
#     }
#     with pytest.raises(HTTPException) as exception:
#         await users.addUser(user)
