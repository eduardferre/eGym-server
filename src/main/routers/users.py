from utils.logger import logging
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from db.mongodb.client import mongodb_client
from db.mongodb.models.user import User
from db.mongodb.schemas.user import users_schema, user_schema
import src.main.routers.usersTO as usersTO
import src.main.routers.posts as posts
import src.main.routers.comments as comments
import src.main.routers.routines as routines


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get(
    "/{attribute}/{value}", response_model=list[User], status_code=status.HTTP_200_OK
)
async def getPublicUsers(attribute: str, value: str):
    logging.info(f"GET /users/{attribute}/{value}")
    list_users = list()
    if attribute == "public" and value == "users":
        list_users = await getUsers()
    elif attribute == "_id":
        list_users.append(await getUserById(value))
    elif attribute == "username":
        list_users.append(await getUserByUsername(value))
    else:
        logging.info("The attribute provided is not valid")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The attribute provided is not valid",
        )

    logging.info("Retrieving user's data taking into account privacy")
    for i, user in enumerate(list_users):
        if type(user) != User:
            user = User(**user)

        if user.public:
            user.email, user.phone = "", ""
        else:
            user.email, user.phone, user.role = "", "", ""
            user.age, user.height, user.weight, user.physicalActivity = 0, 0, 0, 0
            user.routines.clear(), user.routinesLog.clear()
            user.postsLog = list(range(len(user.postsLog)))

        list_users[i] = user

    return list_users


@router.put(
    "/{follower}/{followed}", response_model=list[str], status_code=status.HTTP_200_OK
)
async def followUser(follower: str, followed: str):
    follower_search = await getUserByUsername(follower)
    followed_search = await getUserByUsername(followed)

    if followed in follower_search.following:
        logging.info(f"The user '{follower}' is currently following '{followed}'")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The user '{follower}' is currently following '{followed}'",
        )

    follower_search.following.append(followed)
    followed_search.followers.append(follower)

    follower_response = await updateUser(follower_search)
    await updateUser(followed_search)

    return follower_response.following


@router.put(
    "/{follower}/{unfollowed}", response_model=list[str], status_code=status.HTTP_200_OK
)
async def unfollowUser(follower: str, unfollowed: str):
    follower_search = await getUserByUsername(follower)
    unfollowed_search = await getUserByUsername(unfollowed)

    if not unfollowed in follower_search.following:
        logging.info(f"The user '{follower}' is not following '{unfollowed}'")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The user '{follower}' is not following '{unfollowed}'",
        )

    follower_search.following.remove(unfollowed)
    unfollowed_search.followers.remove(follower)

    follower_response = await updateUser(follower_search)
    await updateUser(unfollowed_search)

    return follower_response.following


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def getUsers():
    logging.info("GET /users/")
    users_list = await search_users()

    if len(users_list) == 0:
        logging.info("There are no users in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no users in the database",
        )
    return users_schema(users_list)


@router.get("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def getUserById(id: str):
    logging.info(f"GET /users/{id}")
    if not ObjectId.is_valid(id):
        logging.info(f"The id provided is not valid")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    user = await search_user("_id", ObjectId(id))

    if type(user) != User:
        logging.info(f"The user with id = {id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = {id} does not exist",
        )
    return user


@router.get("/username/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def getUserByUsername(username: str):
    logging.info(f"GET /users/username/{username}")
    user = await search_user("username", username)

    if type(user) != User:
        logging.info(f"The user {username} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {username} does not exist",
        )
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def addUser(user: User):
    logging.info("POST /users/")
    user_search = await search_user("username", user.username)

    if type(user_search) == User:
        logging.info(f"The username '{user.username}' is already used")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The username '{user.username}' is already used",
        )

    logging.info(
        f"The user {user.username} does not exist in the database and is being processed"
    )

    user_dict = dict(user)
    del user_dict["id"]

    result = await mongodb_client.users.insert_one(user_dict)
    id = result.inserted_id

    logging.info(
        f"The user {user.username} has been inserted correctly in the database"
    )
    new_user = await mongodb_client.users.find_one({"_id": ObjectId(id)})
    return User(**user_schema(new_user))


@router.put("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def updateUser(user: User):
    logging.info("PUT /users/")
    if not ObjectId.is_valid(user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    user_search = await search_user("_id", ObjectId(user.id))

    if user_search == user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The user '{user.username}' has not been updated since there are no changes",
        )

    if type(user_search) != User:
        logging.info(f"The user with id = '{user.id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = '{user.id}' does not exist",
        )

    user_dict = dict(user)
    del user_dict["id"]

    if user.username != user_search.username:
        if type(await search_user("username", user.username)) == User:
            logging.info(f"The username '{user.username}' is already used")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The username '{user.username}' is already used",
            )
        else:
            posts_list = list()
            for post in user.postsLog:
                post.creator = user.username
                post_dict = dict(post)
                await mongodb_client.posts.find_one_and_replace(
                    {"_id": ObjectId(post.id)}, post_dict
                )
                posts_list.append(post_dict)

            comments_list = await comments.getCommentsByCreator(user_search.username)
            for comment in comments_list:
                comment.creator = user.username
                await comments.updateCommentFromPost(comment.postId, comment)

            user_dict["postsLog"] = posts_list
    else:
        posts_list = list()
        for post in user.postsLog:
            post_dict = dict(post)
            posts_list.append(post_dict)

        user_dict["postsLog"] = posts_list

        routines_list = list()
        for routine in user.routinesLog:
            routine_dict = dict(routine)
            routines_list.append(routine_dict)

        user_dict["routinesLog"] = routines_list

    try:
        await mongodb_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict
        )
        logging.info(f"The user with id = {user.id} has been updated")
    except:
        logging.info(f"The user with id = {user.id} has not been updated")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The user with id = {user.id} has not been updated",
        )
    # else:
    #     if user.username != user_search.username:
    #         userTO = await usersTO.getUserTOByUsername(user_search.username)
    #         userTO.username = user.username
    #         await usersTO.updateUserTO(userTO)

    return await search_user("_id", ObjectId(user.id))


@router.delete("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def deleteUser(id: str):
    logging.info(f"DELETE /users/{id}")
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The id provided is not valid",
        )

    user_search = await search_user("_id", ObjectId(id))

    if type(user_search) != User:
        logging.info(f"The user with id = '{id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = '{id}' does not exist",
        )

    try:
        logging.info(f"Deleting user posts")
        await posts.deleteAllCreatorPosts(user_search.username)

        logging.info(f"Deleting user routines")
        await routines.deleteAllCreatorRoutines(user_search.username)

        await mongodb_client.users.find_one_and_delete({"_id": ObjectId(id)})
        logging.info(f"The user with id = {id} has been deleted")
    except:
        for post in user_search.postsLog:
            post_dict = dict(post)
            await mongodb_client.posts.insert_one(post_dict)
        logging.info("Posts have not been deleted")

        for routine in user_search.routinesLog:
            routine_dict = dict(routine)
            await mongodb_client.routines.insert_one(routine_dict)
        logging.info("Routines logs have not been deleted")

        logging.info(f"The user with id = {id} has not been deleted")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The user with id = {id} has not been deleted",
        )
    # else:
    #     userTO = await usersTO.getUserTOByUsername(user_search.username)
    #     await usersTO.deleteUserTO(userTO.id)

    return user_search


@router.delete("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def deleteAllUsers():
    logging.info(f"DELETE /users/")
    list_users = await getUsers()

    logging.info("Massive user deletion has been started")

    for user in list_users:
        user = User(**user)
        await deleteUser(user.id)

    return list_users


# Methods
async def search_user(field: str, key):
    try:
        user = await mongodb_client.users.find_one({field: key})
        if user != None:
            logging.info(f"The user with {field} = {key} exists in the database")
        return User(**user_schema(user))
    except:
        return {"error": f"There's not any user with {field} -> {key}"}


async def search_users():
    users_list = list()
    async for user in mongodb_client.users.find():
        users_list.append(user)
        logging.info(f"({len(users_list)}) -> {user['_id']} - {user['username']}")

    logging.info(f"The number of users found in the database is {len(users_list)}")
    return users_list
