import sys
import os

# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest

from bson import ObjectId
from utils.logger import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.main.routers import transactions

oauth_user = OAuth2PasswordRequestForm(
    grant_type="password", username="edu", password="edu"
)


@pytest.mark.asyncio
async def test_loginUser_Ok():
    login_response = await transactions.login(form_data=oauth_user)
    assert login_response.token_type == "bearer"
    assert login_response.access_token != None
    assert login_response.refresh_token != None
