from pymongo import MongoClient
import environment

# LOCAL DB
# db_client = MongoClient().local

# REMOTE DB
mongodb_client =  MongoClient(
    "mongodb+srv://" + environment.MONGO_USER + ":" + environment.PASSWORD + "@egymcluster.gujw3ru.mongodb.net/").test