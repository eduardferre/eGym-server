from utils.logger import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ddbb.mongodb.client import mongodb_client
from ddbb.mongodb.models.routine import Routine
from ddbb.mongodb.schemas.routine import routines_schema, routine_schema
from ddbb.mongodb.models.user import User
import routers.users as users


router = APIRouter(
    prefix="/routines",
    tags=["routines"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[Routine], status_code=status.HTTP_200_OK)
async def getRoutines():
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
async def getRoutineById(id: str):
    logging.info(f"GET /routines/{id}")
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
async def getRoutinesByCreator(creator: str):
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
async def addRoutine(routine: Routine):
    logging.info("POST /routines/")
    user = await users.search_user("username", routine.creator)
    if type(user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    logging.info(f"The routine is being processed")

    routine_dic = dict(routine)
    del routine_dic["id"]
    
    try:
        result = await mongodb_client.routines.insert_one(routine_dic)
        id = result.inserted_id

        logging.info(f"The routine {ObjectId(id)} has been inserted correctly in the database")
        new_routine = await mongodb_client.routines.find_one({"_id": ObjectId(id)})
    except:
        logging.info("The routine has not been inserted in the database")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The routine has not been inserted in the database",
        )
    return Routine(**routine_schema(new_routine))


@router.put("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def updateRoutine(routine: Routine):
    logging.info("PUT /routines/")
    routine_search = await search_routine("_id", ObjectId(routine.id))

    if type(routine_search) != Routine:
        logging.info(f"The routine with id = '{routine.id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The routine with id = '{routine.id}' does not exist",
        )

    user = await users.search_user("username", routine.creator)
    # user = await mongodb_client.users.find_one({"username": routine.creator})
    if type(user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    dict_comments = list()
    for comment in routine.comments:
        dict_comments.append(dict(comment))
    routine.comments.clear()
    routine.comments = dict_comments

    routine_dic = dict(routine)
    del routine_dic["id"]

    try:
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
    return await search_routine("_id", ObjectId(routine.id))


@router.delete("/{id}", response_model=Routine, status_code=status.HTTP_200_OK)
async def deleteRoutine(id: str):
    logging.info(f"DELETE /routines/{id}")
    routine_search = await search_routine("_id", ObjectId(id))

    if type(routine_search) != Routine:
        logging.info(f"The routine with id = '{id}' does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The routine with id = '{id}' does not exist",
        )

    try:
        logging.info(f"Deleting routine comments")
        await comments.deleteAllRoutineComments(id)

        await mongodb_client.routines.find_one_and_delete({"_id": ObjectId(id)})
        logging.info(f"The routine with id = {id} has been deleted")
    except:
        for comment in routine_search.comments:
            comment_dict = dict(comment)
            await mongodb_client.comments.insert_one(comment_dict)
        logging.info("Comments have not been deleted")

        logging.info(f"The routine with id = {id} has not been deleted")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The routine with id = {id} has not been deleted",
        )
    return routine_search


@router.delete(
    "/creatorRoutines/{creator}", response_model=list[Routine], status_code=status.HTTP_200_OK
)
async def deleteAllCreatorRoutines(creator: str):
    logging.info(f"DELETE /routines/creatorRoutines/{creator}")
    user = await users.search_user("username", creator)
    # user = await mongodb_client.users.find_one({"username": creator})

    if type(user) != User:
        logging.info(f"The user specified does not exist in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user specified does not exist in the database",
        )

    result = await search_routines("creator", creator)

    if len(result) == 0:
        logging.info(f"The user {creator} has no routines, so, anything will be deleted")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {creator} has no routines, so, anything will be deleted",
        )

    routine_search = routines_schema(result)
    routines_list = list()
    for routine in routine_search:
        routines_list.append(await deleteRoutine(routine["id"]))

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
                f"({len(routines_list)}) -> {routine['_id']} - {routine['creator']} - {routine['likes']}"
            )
    else:
        async for routine in mongodb_client.routines.find({field: key}):
            routines_list.append(routine)
            logging.info(
                f"({len(routines_list)}) -> {routine['_id']} - {routine['creator']} - {routine['likes']}"
            )

    logging.info(f"The number of routines found in the database is {len(routines_list)}")
    return routines_list
