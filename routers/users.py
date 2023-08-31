from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ddbb.mongodb.client import db_client
from ddbb.mongodb.models.user import User
from ddbb.mongodb.schemas.user import users_schema, user_schema

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={ status.HTTP_404_NOT_FOUND: { "message": "Not found" } })

@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def getUsers():
    users_list = list()
    user_list = db_client.users.find()
    
    if len(users_list) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="There are no users in the database")
 
    return users_schema(user_list)

@router.get("/{id}") # Call from path /{id}
async def getUserById(id: str):
    user = search_user("_id", ObjectId(id))
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id = {id} does not exist")

    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def addUser(user: User):
    if type(search_user("username", user.username)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user '{user.username}' already exists")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


# Methods
def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({ field: key }))
        return User(**user)
    except:
        return { "error": f"There's not any user with {key}" } 