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

from src.main.routers import comments


@pytest.mark.asyncio
async def test_getComments_NoContent():
    with pytest.raises(HTTPException) as exception:
        await comments.getComments()
    assert isinstance(exception.value, HTTPException)
    assert exception.value.status_code == 204
    assert exception.value.detail == "There are no comments in the database"

# @pytest.mark.order(2)
@pytest.mark.asyncio
async def test_getCommentById_BadRequest():
    idTest = "1"
    with pytest.raises(HTTPException):
        await comments.getCommentById(idTest)
