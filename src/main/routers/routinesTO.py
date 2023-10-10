from fastapi import APIRouter, HTTPException, status
from utils.logger import logging

from db.sqlDB.client import sqlserver_client
from db.sqlDB.models.routineTO import RoutineTO
from db.sqlDB.schemas.routineTO import routineTO_schema
from src.main.routers.exercisesTO import searchExerciseTO

sql_cursor = sqlserver_client.cursor()
sql_cursor_async = sqlserver_client.cursor()

router = APIRouter(
    prefix="/routinesTO",
    tags=["routinesTO"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[RoutineTO], status_code=status.HTTP_200_OK)
async def getRoutinesTO():
    logging.info(f"GET /routinesTO/")

    query = f"SELECT * FROM dbo.routines"
    sql_cursor.execute(query)
    routines_list = list()
    routine_response = sql_cursor.fetchall()

    if len(routine_response) == 0:
        logging.info("There are no routines in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no routines in the database",
        )

    for routine in routine_response:
        routines_list.append(
            RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))
        )
    return routines_list


@router.get("/{id}", response_model=RoutineTO, status_code=status.HTTP_200_OK)
async def getRoutineTOById(id: int):
    logging.info(f"GET /routinesTO/{id}")

    query = f"SELECT * FROM dbo.routines\
                WHERE id={id}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()

    if routine == None:
        logging.info(f"The routine with id = {id} is not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The routine with id = {id} is not found",
        )

    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))


@router.get(
    "/creator/{creator}", response_model=list[RoutineTO], status_code=status.HTTP_200_OK
)
async def getRoutinesTOByCreator(creator: str):
    logging.info(f"GET /routinesTO/{creator}")

    query = f"SELECT * FROM dbo.routines\
                WHERE creator='{creator}'"
    routines_list = list()
    sql_cursor.execute(query)
    routine_response = sql_cursor.fetchall()

    if len(routine_response) == 0:
        logging.info(f"There are no routines made by {creator}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There are no routines made by {creator}",
        )

    for routine in routine_response:
        routines_list.append(
            RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))
        )
    return routines_list


@router.get(
    "/routineName/{name}",
    response_model=list[RoutineTO],
    status_code=status.HTTP_200_OK,
)
async def getRoutinesTOByName(name: str):
    logging.info(f"GET /routinesTO/{name}")

    query = f"SELECT * FROM dbo.routines\
                WHERE name='{name}'"
    routines_list = list()
    sql_cursor.execute(query)
    routine_response = sql_cursor.fetchall()

    if len(routine_response) == 0:
        logging.info(f"There are not any routine named: {name}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There are not any routine named: {name}",
        )

    for routine in routine_response:
        routines_list.append(
            RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))
        )
    return routines_list


@router.post("/", response_model=RoutineTO, status_code=status.HTTP_201_CREATED)
async def addRoutineTO(routineTO: RoutineTO):
    logging.info(f"POST /routinesTO/")

    query = f"INSERT dbo.routines (creator, name, description)\
                OUTPUT INSERTED.*\
                VALUES ('{routineTO.creator}', '{routineTO.name}', '{routineTO.description}')"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    sqlserver_client.commit()
    logging.info(
        f"The routine {routineTO.name} has been inserted correctly in the database"
    )

    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))


@router.post(
    "/{routineId}_{exerciseId}",
    response_model=RoutineTO,
    status_code=status.HTTP_201_CREATED,
)
async def addExerciseTOToRoutineTO(routineId: int, exerciseId: int):
    logging.info(f"POST /routinesTO/{routineId}_{exerciseId}")

    query = f"SELECT * FROM dbo.exercises\
                WHERE id={exerciseId}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    if exercise == None:
        logging.info(f"The exercise with id = {exerciseId} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise with id = {exerciseId} does not exist",
        )

    query = f"SELECT * FROM dbo.routines\
                WHERE id={routineId}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    if routine == None:
        logging.info(f"The routine with id = {routineId} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The routine with id = {routineId} does not exist",
        )

    query = f"SELECT * FROM dbo.relationRoutinesExercises\
                WHERE routineId={routineId} AND exerciseId={exerciseId}"
    sql_cursor.execute(query)
    relation = sql_cursor.fetchone()
    if relation != None:
        logging.info("The exercise is already in the routine")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The exercise is already in the routine",
        )

    logging.info("The exercise is being added to the specified routine")

    query = f"INSERT dbo.relationRoutinesExercises (routineId, exerciseId)\
                VALUES ('{routineId}', '{exerciseId}')"
    sql_cursor.execute(query)
    sqlserver_client.commit()

    logging.info(
        f"The exercise with id = {exerciseId} has been added to routine with id = {routineId}"
    )

    return searchRoutineTO("id", routineId)


@router.put("/", response_model=RoutineTO, status_code=status.HTTP_201_CREATED)
async def updateRoutineTO(routineTO: RoutineTO):
    logging.info(f"PUT /routinesTO/")

    routine_search = searchRoutineTO("id", routineTO.id)
    if type(routine_search) != RoutineTO:
        logging.info(routine_search["error"])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=routine_search["error"]
        )

    logging.info("The routine is being updated")

    query = f"UPDATE dbo.routines\
                SET creator = '{routineTO.creator}', name = '{routineTO.name}', description = '{routineTO.description}'\
                OUTPUT INSERTED.*\
                WHERE id={routineTO.id}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    sqlserver_client.commit()

    logging.info(f"The routine with id = {routineTO.id} has been updated")

    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))


@router.delete("/{id}", response_model=RoutineTO, status_code=status.HTTP_200_OK)
async def deleteRoutineTO(id: int):
    logging.info(f"DELETE /routinesTO/{id}")

    routine_search = searchRoutineTO("id", id)
    if type(routine_search) != RoutineTO:
        logging.info(routine_search["error"])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=routine_search["error"]
        )

    logging.info("The routine is being deleted")

    query = f"DELETE FROM dbo.relationRoutinesExercises\
                WHERE routineId={id}"
    sql_cursor.execute(query)

    query = f"DELETE FROM dbo.routines\
                OUTPUT DELETED.*\
                WHERE id={id}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    sqlserver_client.commit()

    logging.info(f"The routine with id = {id} has been deleted")

    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))


# Methods
def searchRoutineTO(field: str, key):
    query = f"SELECT * FROM dbo.routines\
                WHERE {field}='{key}'"
    try:
        sql_cursor.execute(query)
        routine = sql_cursor.fetchone()
        return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))
    except:
        return {"error": f"The routine with {field} = '{key}' does not exist"}


def tupleRoutineTOToDict(routine: dict):
    exercises_list = searchRoutineExercises(routine[0])

    routine_dict = dict(
        {
            "_id": str(routine[0]),
            "creator": routine[1],
            "name": routine[2],
            "description": routine[3],
            "exercises": exercises_list,
        }
    )

    return routine_dict


def searchRoutineExercises(
    routineId: int,
):  # A way to populate RoutineTO object with ExerciseTO objects
    query = f"SELECT exerciseId FROM dbo.relationRoutinesExercises\
                WHERE routineId={routineId}"
    exercisesId_list = list()
    sql_cursor_async.execute(query)
    exerciseId_response = sql_cursor_async.fetchall()

    for exerciseId in exerciseId_response:
        exercisesId_list.append(exerciseId[0])

    exercises_list = list()

    for exerciseId in exercisesId_list:
        exercises_list.append(searchExerciseTO("id", exerciseId))

    return exercises_list
