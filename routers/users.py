import logging
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ddbb.mongodb.client import mongodb_client
from ddbb.mongodb.models.user import User
from ddbb.mongodb.schemas.user import users_schema, user_schema


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def getUsers():
    logging.info("GET /users/")
    users_list = await search_users()

    if len(users_list) == 0:
        logging.info("Thre are no users in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no users in the database",
        )

    return users_schema(users_list)


@router.get("/{id}")  # Call from path /{id}
async def getUserById(id: str):
    logging.info(f"GET /users/{id}")
    user = search_user("_id", ObjectId(id))

    if user == None:
        logging.info(f"The user with id = {id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = {id} does not exist",
        )

    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def addUser(user: User):
    logging.info("POST /users/")
    user_search = search_user("_id", ObjectId(user.id))

    if type(user_search) == User:
        if user.id == user_search.id:
            logging.info(f"The user with id = '{user.id}' already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The user with id = '{user.id}' already exists",
            )

        if user.username == user_search.username:
            logging.info(f"The username '{user.username}' is already used")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The username '{user.username}' is already used",
            )

    logging.info(
        f"The username {user.username} does not exist in the database and is being processed"
    )

    user_dict = dict(user)
    del user_dict["id"]

    id = mongodb_client.users.insert_one(user_dict).inserted_id
    logging.info(
        f"The user {user.username} has been inserted correctly in the database"
    )

    new_user = user_schema(mongodb_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def updateUser(user: User):
    logging.info("PUT /users/")
    user_search = search_user("_id", ObjectId(user.id))

    if type(user_search) != User:
        logging.info(f"The user with id = '{user.id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = '{user.id}' does not exist",
        )

    if user.username == user_search.username:
        logging.info(f"The username '{user.username}' is already used")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The username '{user.username}' is already used",
        )

    user_dict = dict(user)
    del user_dict["id"]

    try:
        mongodb_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        logging.info(f"The user with id = {user.id} has been updated")
    except:
        logging.info(f"The user with id = {user.id} has not been updated")
        return {"error": f"The user with id = {user.id} has not been updated"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def deleteUser(id: str):
    logging.info(f"DELETE /users/{id}")
    user_search = search_user("_id", ObjectId(id))

    if type(user_search) != User:
        logging.info(f"The user with id = '{id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = '{id}' does not exist",
        )

    try:
        mongodb_client.users.find_one_and_delete({"_id": ObjectId(id)})
        logging.info(f"The user with id = {id} has been deleted")
    except:
        logging.info(f"The user with id = {id} has not been deleted")
        return {"error": f"The user with id = {id} has not been deleted"}

    return user_search


# Methods
def search_user(field: str, key):
    try:
        user = user_schema(mongodb_client.users.find_one({field: key}))
        logging.info(f"The user with {field} = {key} exists in the database")
        return User(**user)
    except:
        return {"error": f"There's not any user with {field} -> {key}"}


async def search_users():
    users_list = list()
    async for user in mongodb_client.users.find():
        users_list.append(user)
        logging.info(f"({len(users_list)}) -> {user['_id']} - {user['username']}")
        
    logging.info(f"The number of users found in the database is {len(users_list)}")
    return users_list