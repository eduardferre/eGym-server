import src.main.services.auth as auth_handler_class

from utils.logger import logging

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from typing import Optional

from db.mongodb.client import mongodb_client
from db.mongodb.models.routine import Routine
from db.mongodb.models.exercise import Exercise
from db.mongodb.models.set import Set
from db.mongodb.schemas.routine import routines_schema, routine_schema
from db.mongodb.models.user import User
import src.main.routers.users as users

oauth2_scheme = OAuth2PasswordBearer("/transactions/login")
auth_handler = auth_handler_class.Auth()


def token_validation(token: str):
    return auth_handler.decode_token(token)


router = APIRouter(
    prefix="/routines",
    tags=["routines"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[Routine], status_code=status.HTTP_200_OK)
async def getRoutines(token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info("GET /routines/")
        routines_list = await search_routines(None, None)

        if len(routines_list) == 0:
            logging.info("There are no routines in the database")
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="There are no routines in the database",
            )
        return routines_schema(routines_list)


@router.get("/{id}", response_model=Routine, status_code=status.HTTP_200_OK)
async def getRoutineById(id: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"GET /routines/{id}")
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        routine = await search_routine("_id", ObjectId(id))
        if type(routine) != Routine:
            logging.info(f"The routine with id = {id} does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The routine with id = {id} does not exist",
            )

        return await search_routine("_id", ObjectId(id))


@router.get(
    "/creator/{creator}", response_model=list[Routine], status_code=status.HTTP_200_OK
)
async def getRoutinesByCreator(creator: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"GET /routines/creator/{creator}")
        user = await users.search_user("username", creator)
        if type(user) != User:
            logging.info(f"The user specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user specified does not exist in the database",
            )

        routines_list = await search_routines("creator", creator)

        if len(routines_list) == 0:
            logging.info("There are no routines in the database made by this user")
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="There are no routines in the database made by this user",
            )
        return routines_schema(routines_list)


@router.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def addRoutine(routine: Routine, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info("POST /routines/")

        user = await users.search_user("username", routine.creator)
        if type(user) != User:
            logging.info(f"The user specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user specified does not exist in the database",
            )

        logging.info(f"The routine is being processed")

        dict_exercises = list()
        for exercise in routine.exercises:
            exercise.id = ObjectId()
            dict_sets = list()
            for set in exercise.sets:
                set.id = ObjectId()
                dict_sets.append(dict(set))
            exercise.sets.clear()
            exercise.sets = dict_sets
            dict_exercises.append(dict(exercise))
        routine.exercises.clear()
        routine.exercises = dict_exercises

        routine_dic = dict(routine)
        copy_routine_dict = routine_dic.copy()
        del routine_dic["id"]

        try:
            user_search = await users.getUserByUsername(routine.creator, token)

            result = await mongodb_client.routines.insert_one(routine_dic)
            id = result.inserted_id

            logging.info(
                f"The routine {ObjectId(id)} has been inserted correctly in the database"
            )
            new_routine = await mongodb_client.routines.find_one({"_id": ObjectId(id)})
        except:
            logging.info("The routine has not been inserted in the database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The routine has not been inserted in the database",
            )
        else:
            copy_routine_dict["id"] = str(id)
            user_search.routinesLog.append(copy_routine_dict)
            await users.updateUser(user_search, token)
            logging.info(f"Routine logs of '{user_search.username}' has been updated")

        return Routine(**routine_schema(new_routine))


@router.put("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def updateRoutine(routine: Routine, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info("PUT /routines/")
        if not ObjectId.is_valid(routine.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        routine_search = await search_routine("_id", ObjectId(routine.id))

        routine.id = str(routine.id)
        for exercise in routine.exercises:
            exercise["id"] = str(exercise["id"])
            for set in exercise["sets"]:
                set["id"] = str(set["id"])
        routine = Routine.parse_raw(routine.json())

        if routine.__eq__(routine_search):
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"The routine '{routine.id}' has not been updated since there are no changes",
            )

        if type(routine_search) != Routine:
            logging.info(f"The routine with id = '{routine.id}' does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The routine with id = '{routine.id}' does not exist",
            )

        user = await users.search_user("username", routine.creator)
        if type(user) != User:
            logging.info(f"The user specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user specified does not exist in the database",
            )

        dict_exercises = list()
        for exercise in routine.exercises:
            dict_sets = list()
            for set in exercise.sets:
                dict_sets.append(dict(set))
            exercise.sets.clear()
            exercise.sets = dict_sets
            dict_exercises.append(dict(exercise))
        routine.exercises.clear()
        routine.exercises = dict_exercises

        routine_dic = dict(routine)
        del routine_dic["id"]

        try:
            user_search = await users.getUserByUsername(routine_search.creator, token)

            await mongodb_client.routines.find_one_and_replace(
                {"_id": ObjectId(routine.id)}, routine_dic
            )
            logging.info(f"The routine with id = {routine.id} has been updated")
        except Exception as e:
            print(e)
            logging.info(f"The routine with id = {routine.id} has not been updated")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The routine with id = {routine.id} has not been updated",
            )
        else:
            for routine_for in user_search.routinesLog:
                if routine_for.id == routine.id:
                    index = user_search.routinesLog.index(routine_for)
                    user_search.routinesLog.insert(index, routine)
                    user_search.routinesLog.remove(routine_for)

            await users.updateUser(user_search, token)
            logging.info(f"Routine logs of '{user_search.username}' has been updated")
        return await search_routine("_id", ObjectId(routine.id))


@router.delete("/{id}", response_model=Routine, status_code=status.HTTP_200_OK)
async def deleteRoutine(id: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"DELETE /routines/{id}")
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The id provided is not valid",
            )

        routine_search = await search_routine("_id", ObjectId(id))

        if type(routine_search) != Routine:
            logging.info(f"The routine with id = '{id}' does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The routine with id = '{id}' does not exist",
            )

        try:
            user_search = await users.getUserByUsername(routine_search.creator, token)

            await mongodb_client.routines.find_one_and_delete({"_id": ObjectId(id)})
            logging.info(f"The routine with id = {id} has been deleted")
        except:
            logging.info(f"The routine with id = {id} has not been deleted")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The routine with id = {id} has not been deleted",
            )
        else:
            for routine in user_search.routinesLog:
                if routine.id == id:
                    user_search.routinesLog.remove(routine)

            await users.updateUser(user_search, token)
            logging.info(f"Routine logs of '{user_search.username}' has been updated")
        return routine_search


@router.delete(
    "/creatorRoutines/{creator}",
    response_model=list[Routine],
    status_code=status.HTTP_200_OK,
)
async def deleteAllCreatorRoutines(creator: str, token: str = Depends(oauth2_scheme)):
    if token_validation(token) != None:
        logging.info(f"DELETE /routines/creatorRoutines/{creator}")
        user = await users.search_user("username", creator)

        if type(user) != User:
            logging.info(f"The user specified does not exist in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The user specified does not exist in the database",
            )

        result = await search_routines("creator", creator)
        routines_list = list()

        if len(result) == 0:
            logging.info(
                f"The user {creator} has no routines, so, anything will be deleted"
            )
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND,
            #     detail=f"The user {creator} has no routines, so, anything will be deleted",
            # )
        else:
            logging.info(f"The {creator} routines will be deleted")
            routine_search = routines_schema(result)
            for routine in routine_search:
                routines_list.append(await deleteRoutine(routine["id"], token))

        return routines_list


# Methods
async def search_routine(field: str, key):
    try:
        routine = await mongodb_client.routines.find_one({field: key})
        logging.info(f"The routine with {field} = {key} exists in the database")
        return Routine(**routine_schema(routine))
    except:
        return {"error": f"There's not any routine with {field} -> {key}"}


async def search_routines(field: Optional[str], key: Optional[any]):
    routines_list = list()
    if (field and key) == None:
        async for routine in mongodb_client.routines.find():
            routines_list.append(routine)
            logging.info(
                f"({len(routines_list)}) -> {routine['_id']} - {routine['creator']} - {routine['name']}"
            )
    else:
        async for routine in mongodb_client.routines.find({field: key}):
            routines_list.append(routine)
            logging.info(
                f"({len(routines_list)}) -> {routine['_id']} - {routine['creator']} - {routine['name']}"
            )

    logging.info(
        f"The number of routines found in the database is {len(routines_list)}"
    )
    return routines_list
