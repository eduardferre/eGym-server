from fastapi import APIRouter, HTTPException, status
from utils.logger import logging

from db.sqlDB.client import sqlserver_client
from db.sqlDB.models.exerciseTO import ExerciseTO
from db.sqlDB.schemas.exerciseTO import exerciseTO_schema

sql_cursor = sqlserver_client.cursor()

router = APIRouter(
    prefix="/exercisesTO",
    tags=["exercisesTO"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[ExerciseTO], status_code=status.HTTP_200_OK)
async def getExercisesTO():
    logging.info(f"GET /exercisesTO/")

    query = f"SELECT * FROM dbo.exercises"
    sql_cursor.execute(query)
    exercises_list = list()
    exercise_response = sql_cursor.fetchall()

    if len(exercise_response) == 0:
        logging.info("There are no exercises in the database")
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no exercises in the database",
        )

    for exercise in exercise_response:
        exercises_list.append(
            ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))
        )
    return exercises_list


@router.get("/{id}", response_model=ExerciseTO, status_code=status.HTTP_200_OK)
async def getExerciseTOById(id: int):
    logging.info(f"GET /exercisesTO/{id}")

    query = f"SELECT * FROM dbo.exercises\
                WHERE id={id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()

    if exercise == None:
        logging.info(f"The exercise with id = {id} is not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise with id = {id} is not found",
        )

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.get(
    "/creator/{creator}",
    response_model=list[ExerciseTO],
    status_code=status.HTTP_200_OK,
)
async def getExercisesTOByCreator(creator: str):
    logging.info(f"GET /exercisesTO/{creator}")

    query = f"SELECT * FROM dbo.exercises\
                WHERE creator='{creator}'"
    sql_cursor.execute(query)
    exercises_list = list()
    exercise_response = sql_cursor.fetchall()

    if len(exercise_response) == 0:
        logging.info(f"The user {creator} has not created any exercises yet")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {creator} has not created any exercises yet",
        )

    for exercise in exercise_response:
        exercises_list.append(
            ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))
        )
    return exercises_list


@router.get(
    "/exerciseName/{name}", response_model=ExerciseTO, status_code=status.HTTP_200_OK
)
async def getExerciseTOByName(name: str):
    logging.info(f"GET /exercisesTO/{name}")

    query = f"SELECT * FROM dbo.exercises\
                WHERE name='{name}'"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()

    if exercise == None:
        logging.info(f"The exercise {name} is not found in the list of exercises")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise {name} is not found in the list of exercises",
        )

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.post("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def addExerciseTO(exerciseTO: ExerciseTO):
    logging.info(f"POST /exercisesTO/")

    if type(searchExerciseTO("id", exerciseTO.id)) == ExerciseTO:
        logging.info(f"The exercise with id = {exerciseTO.id} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The exercise with id = {exerciseTO.id} already exists",
        )

    logging.info("The exercise does not exist in the database and is being processed")

    query = f"INSERT dbo.exercises (creator, name, description)\
                OUTPUT INSERTED.*\
                VALUES ('{exerciseTO.creator}', '{exerciseTO.name}', '{exerciseTO.description}')"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    logging.info(
        f"The exercise {exerciseTO.name} has been inserted correctly in the database"
    )

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.put("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def updateExerciseTO(exerciseTO: ExerciseTO):
    logging.info(f"PUT /exercisesTO/")

    exercise_search = searchExerciseTO("id", exerciseTO.id)
    if type(exercise_search) != ExerciseTO:
        logging.info(f"The exercise with id = {exerciseTO.id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise with id = {exerciseTO.id} does not exist",
        )

    logging.info("The exercise is being updated")

    query = f"UPDATE dbo.exercises\
                SET creator = '{exerciseTO.creator}', name = '{exerciseTO.name}', description = '{exerciseTO.description}'\
                OUTPUT INSERTED.*\
                WHERE id={exerciseTO.id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    logging.info(f"The exercise {exerciseTO.name} has been updated correctly")

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.delete("/{id}", response_model=ExerciseTO, status_code=status.HTTP_200_OK)
async def deleteExerciseTO(id: int):
    logging.info(f"DELETE /exercisesTO/{id}")
    exercise_search = searchExerciseTO("id", id)

    if type(exercise_search) != ExerciseTO:
        logging.info(f"The exercise with id = {id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise with id = {id} does not exist",
        )

    logging.info("The exercise is being deleted")

    query = f"DELETE FROM dbo.relationRoutinesExercises\
                WHERE exerciseId={id}"
    sql_cursor.execute(query)
    query = f"DELETE FROM dbo.exercises\
                OUTPUT DELETED.*\
                WHERE id={id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    logging.info(f"The exercise {exercise_search.name} has been deleted")

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


# Methods
def searchExerciseTO(field: str, key):
    query = f"SELECT * FROM dbo.exercises\
                WHERE {field}='{key}'"
    try:
        sql_cursor.execute(query)
        exercise = sql_cursor.fetchone()
        return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))
    except:
        return {"error": f"The exercise with {field} = '{key}' does not exist"}


def tupleExerciseTOToDict(exercise: dict):
    exercise_dict = dict(
        {
            "_id": str(exercise[0]),
            "creator": exercise[1],
            "name": exercise[2],
            "description": exercise[3],
        }
    )
    return exercise_dict
