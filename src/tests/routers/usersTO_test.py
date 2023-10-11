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
from uuid import uuid4

from db.sqlDB.models.userTO import UserTO
from src.main.routers import usersTO

id_test_404 = uuid4()


@pytest.mark.asyncio
async def test_getUsersTO_NoContent():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUsersTO()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204


@pytest.mark.asyncio
async def test_getUserTOById_NotFound():
    with pytest.raises(HTTPException) as exception:
        logging.critical(id_test_404)
        await usersTO.getUserTOById(id_test_404)
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404


@pytest.mark.asyncio
async def test_getUserByUsername_NotFound():
    with pytest.raises(HTTPException) as exception:
        await usersTO.getUserTOByUsername("eduardferre")
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 404
