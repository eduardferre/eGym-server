import sys
import os


# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append("/Users/eduardfer/Desktop/TFG TELEMÀTICA/eGym-server/src")

os.environ["TEST_ENABLED"] = "TRUE"

import pytest

from fastapi import status
from fastapi.testclient import TestClient
from src.main import app

from tests.routers import comments_test

client = TestClient(app)  # uvicorn main:app --reload


# @pytest.mark.asyncio
# async def test_all():
#     await comments_test.initTests()