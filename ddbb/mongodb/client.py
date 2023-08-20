from pymongo import MongoClient
import environment_variables

# LOCAL DB
# db_client = MongoClient().local

# REMOTE DB
db_client =  MongoClient(
    "mongodb+srv://" + environment_variables.MONGO_USER + ":" + environment_variables.PASSWORD + "@egymcluster.gujw3ru.mongodb.net/").test