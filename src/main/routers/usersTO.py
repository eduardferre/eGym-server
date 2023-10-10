import logging
import os
from fastapi import APIRouter, HTTPException, status

from db.sqlDB.client import sqlserver_client
from db.sqlDB.models.userTO import UserTO
from db.sqlDB.models.exerciseTO import ExerciseTO
from db.sqlDB.models.routineTO import RoutineTO
from db.sqlDB.schemas.userTO import userTO_schema, usersTO_schema

import src.main.routers.exercisesTO as exercisesTO
import src.main.routers.routinesTO as routinesTO

sql_cursor = sqlserver_client.cursor()

router = APIRouter(
    prefix="/usersTO",
    tags=["usersTO"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[UserTO], status_code=status.HTTP_200_OK)
async def getUsersTO():
    logging.info(f"GET /usersTO/")

    query = f"SELECT * FROM dbo.users"
    sql_cursor.execute(query)
    users_list = list()
    user = sql_cursor.fetchone()

    if user == None:
        logging.info("There are no users in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no users in the database",
        )

    while user:
        users_list.append(UserTO(**userTO_schema(tupleUserTOToDict(user))))
        user = sql_cursor.fetchone()
    return users_list


@router.get("/{id}", response_model=UserTO, status_code=status.HTTP_200_OK)
async def getUserTOById(id: int):
    logging.info(f"GET /usersTO/{id}")

    query = f"SELECT * FROM dbo.users\
                WHERE id={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()

    if user == None:
        logging.info(f"The user with id = {id} is not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = {id} is not found",
        )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.get("/{username}", response_model=UserTO, status_code=status.HTTP_200_OK)
async def getUserTOByUsername(username: str):
    logging.info(f"GET /usersTO/{username}")

    query = f"SELECT * FROM dbo.users\
                WHERE username='{username}'"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()

    if user == None:
        logging.info(f"The user with username = {username} is not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with username = {username} is not found",
        )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.post("/", response_model=UserTO, status_code=status.HTTP_201_CREATED)
async def addUserTO(userTO: UserTO):
    logging.info(f"POST /usersTO/")

    if type(searchUserTO("id", userTO.id)) == UserTO:
        logging.info(f"The user with id = {userTO.id} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with id = {userTO.id} already exists",
        )

    logging.info(
        f"The user {userTO.username} does not exist in the database and is being processed"
    )

    query = f"INSERT dbo.users (username, firstName, lastName, email, password, birthDate)\
                OUTPUT INSERTED.*\
                VALUES ('{userTO.username}', '{userTO.firstname}', '{userTO.lastname}', '{userTO.email}', '{userTO.password}', '{userTO.birthDate}')"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()

    logging.info(
        f"The user {userTO.username} has been inserted correctly in the database"
    )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.put("/", response_model=UserTO, status_code=status.HTTP_201_CREATED)
async def updateUserTO(userTO: UserTO):
    logging.info(f"PUT /usersTO/")

    user_search = searchUserTO("id", userTO.id)
    if type(user_search) != UserTO:
        logging.info(user_search["error"])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_search["error"]
        )

    # if user.username != user_search.username:
    #     if type(await searchUserTO("username", user.username)) == UserTO:
    #         logging.info(f"The username '{user.username}' is already used")
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"The username '{user.username} is already used",
    #         )

    logging.info(f"The user {userTO.username} is being updated")

    query = f"UPDATE dbo.users\
                SET username = '{userTO.username}', firstName = '{userTO.firstname}', lastName = '{userTO.lastname}', email = '{userTO.email}', password = '{userTO.password}', birthDate = '{userTO.birthDate}'\
                OUTPUT INSERTED.*\
                WHERE id={userTO.id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()

    # if user.username != user_search.username:
    #     list_exercisesTO = exercisesTO.getExercisesTOByCreator(user_search.username)
    #     for exerciseTO in list_exercisesTO:
    #         exerciseTO = ExerciseTO(**exerciseTO)
    #         exerciseTO.creator = user.username
    #         await exercisesTO.updateExerciseTO(exerciseTO)

    #     list_routinesTO = routinesTO.getRoutinesTOByCreator(user_search.username)
    #     for routineTO in list_routinesTO:
    #         routineTO = RoutineTO(**routineTO)
    #         routineTO.creator = user.username
    #         await routinesTO.updateRoutineTO(routineTO)

    logging.info(
        f"The user {userTO.username} has been updated, as well as the exercises and routines that belong to him/her"
    )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.delete("/{id}", response_model=UserTO, status_code=status.HTTP_200_OK)
async def deleteUserTO(id: int):
    logging.info(f"DELETE /usersTO/{id}")

    user_search = searchUserTO("id", id)
    if type(user_search) != UserTO:
        logging.info(user_search["error"])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_search["error"]
        )

    logging.info(f"The user with id = {id} is being deleted")

    query = f"DELETE FROM dbo.users\
                OUTPUT DELETED.*\
                WHERE id={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()

    # list_exercisesTO = exercisesTO.getExercisesTOByCreator(user_search.username)
    # for exerciseTO in list_exercisesTO:
    #     exerciseTO = ExerciseTO(**exerciseTO)
    #     exerciseTO.creator = "unknown"
    #     await exercisesTO.updateExerciseTO(exerciseTO)

    # list_routinesTO = routinesTO.getRoutinesTOByCreator(user_search.username)
    # for routineTO in list_routinesTO:
    #     routineTO = RoutineTO(**routineTO)
    #     routineTO.creator = "unknown"
    #     await routinesTO.updateRoutineTO(routineTO)

    logging.info(
        f"The user with id = {id} has been deleted and all the exercises and routines that belong to him/her are updated to: creator='unknown'"
    )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


# Methods
def searchUserTO(field: str, key):
    query = f"SELECT * FROM dbo.users\
                WHERE {field}='{key}'"
    try:
        sql_cursor.execute(query)
        user = sql_cursor.fetchone()
        return UserTO(**userTO_schema(tupleUserTOToDict(user)))
    except:
        return {"error": f"The user with {field} = '{key}' does not exist"}


def tupleUserTOToDict(user: dict):
    user_dict = dict(
        {
            "_id": str(user[0]),
            "username": user[1],
            "firstname": user[2],
            "lastname": user[3],
            "email": user[4],
            "password": user[5],
            "birthDate": str(user[6]),
        }
    )
    return user_dict
