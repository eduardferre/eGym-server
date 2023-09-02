import asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils import environment

# LOCAL DB
# mongodb_client = AsyncIOMotorClient(
#     "mongodb://localhost:27017/",
#     server_api=ServerApi("1")
# ).egym

# REMOTE DB
mongodb_client = AsyncIOMotorClient(
    "mongodb+srv://"
    + environment.MONGO_USER
    + ":"
    + environment.MONGO_PASSWORD
    + "@egymcluster.gujw3ru.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
    server_api=ServerApi("1"),
).test
