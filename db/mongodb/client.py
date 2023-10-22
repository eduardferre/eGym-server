import os
import asyncio
import certifi
from utils.logger import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv

load_dotenv()

# LOCAL DB
if os.getenv("TEST_ENABLED") == "FALSE":
    logging.info("Local eGym database running")
    mongodb_client = AsyncIOMotorClient(
        "mongodb://localhost:27017/", server_api=ServerApi("1")
    ).egym
else:
    logging.info("Test eGym database running")
    mongodb_client = AsyncIOMotorClient(
        "mongodb://localhost:27017/", server_api=ServerApi("1")
    ).egymTest

# REMOTE DB
# mongodb_client = AsyncIOMotorClient(
#     "mongodb+srv://"
#     + os.getenv("MONGO_USER")
#     + ":"
#     + os.getenv("MONGO_PASSWORD")
#     + "@egymcluster.gujw3ru.mongodb.net/?retryWrites=true&w=majority",
#     tlsCAFile=certifi.where(),
#     server_api=ServerApi("1"),
# ).test
