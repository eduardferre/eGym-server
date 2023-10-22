import sys
import os

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest
from datetime import datetime, date

from bson import ObjectId
from utils.logger import logging
from fastapi import APIRouter, HTTPException, status
from uuid import uuid4

from db.sqlDB.models.userTO import UserTO
from src.main.routers import usersTO

id_test_404 = str(uuid4())
userTO_add = UserTO(
    **{
        "id": "string",
        "username": "eduardferre",
        "firstname": "Eduard",
        "lastname": "Ferre",
        "email": "eduardferre@gmail.es",
        "password": "string",
        "birthDate": date(2000, 4, 7).strftime("%Y-%m-%d"),
    }
)


@pytest.mark.asyncio
async def test_getUsersTO_NoContent():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUsersTO()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_getUserTOById_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUserTOById("id_not_valid")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_getUserTOById_NotFound():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUserTOById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_getUserTOByUsername_NotFound():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUserTOByUsername("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_addUserTO_Created():
    user_response = await usersTO.addUserTO(userTO_add)
    userTO_add.id = user_response.id
    assert isinstance(user_response, UserTO)
    assert user_response.username == "eduardferre"

    user_add_new = userTO_add.model_copy()
    user_add_new.username = "test2"
    await usersTO.addUserTO(user_add_new)


@pytest.mark.asyncio
async def test_addUserTO_Conflict():
    with pytest.raises(HTTPException) as exception:
        await usersTO.addUserTO(userTO_add)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.asyncio
async def test_getUserTO_Ok():
    users_list = await usersTO.getUsersTO()
    assert isinstance(users_list, list)
    assert len(users_list) > 0


@pytest.mark.asyncio
async def test_getUserTOById_Ok():
    user_response = await usersTO.getUserTOById(userTO_add.id)
    assert isinstance(user_response, UserTO)
    assert user_response.id == userTO_add.id


@pytest.mark.asyncio
async def test_getUserTOByUsername_Ok():
    user_response = await usersTO.getUserTOByUsername("eduardferre")
    assert isinstance(user_response, UserTO)
    assert user_response.id == userTO_add.id


@pytest.mark.asyncio
async def test_updateUserTO_BadRequest():
    user_not_valid_id = userTO_add.model_copy()
    user_not_valid_id.id = "not_valid_id"
    with pytest.raises(HTTPException) as exception:
        await usersTO.updateUserTO(user_not_valid_id)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_updateUserTO_NotFound():
    user_not_found = userTO_add.model_copy()
    user_not_found.id = id_test_404
    with pytest.raises(HTTPException) as exception:
        await usersTO.updateUserTO(user_not_found)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_updateUserTO_Conflict():
    user_not_found = userTO_add.model_copy()
    user_not_found.username = "test2"
    with pytest.raises(HTTPException) as exception:
        await usersTO.updateUserTO(user_not_found)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 409


@pytest.mark.asyncio
async def test_updateUserTO_Ok():
    user_update = userTO_add.model_copy()
    user_update.username = "eduardfer"
    user_response = await usersTO.updateUserTO(user_update)
    assert isinstance(user_response, UserTO)
    assert user_response.id == user_update.id
    assert user_response.username == user_update.username


@pytest.mark.asyncio
async def test_deleteUserTO_BadRequest():
    with pytest.raises(HTTPException) as exception:
        await usersTO.deleteUserTO("not_valid_id")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 400


@pytest.mark.asyncio
async def test_deleteUserTO_NotFound():
    with pytest.raises(HTTPException) as exception:
        await usersTO.deleteUserTO(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_deleteUserTO_Ok():
    user_to_delete = await usersTO.getUserTOByUsername("eduardfer")
    user_response = await usersTO.deleteUserTO(user_to_delete.id)
    assert isinstance(user_response, UserTO)
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUserTOByUsername("eduardfer")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404
