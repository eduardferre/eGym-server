from fastapi import APIRouter, HTTPException, status

from src.db.sqlDB.client import sqlserver_client
from src.db.sqlDB.models.exerciseTO import ExerciseTO
from src.db.sqlDB.schemas.exerciseTO import exerciseTO_schema

sql_cursor = sqlserver_client.cursor()

router = APIRouter(
    prefix="/exercisesTO",
    tags=["exercisesTO"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[ExerciseTO], status_code=status.HTTP_200_OK)
async def getExercisesTO():
    query = f"SELECT * FROM dbo.exercises"
    sql_cursor.execute(query)
    exercises_list = list()
    exercise_response = sql_cursor.fetchall()

    if len(exercise_response) == 0:
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
    query = f"SELECT * FROM dbo.exercises\
                WHERE id={id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()

    if exercise == None:
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
    query = f"SELECT * FROM dbo.exercises\
                WHERE creator='{creator}'"
    sql_cursor.execute(query)
    exercises_list = list()
    exercise_response = sql_cursor.fetchall()

    if len(exercise_response) == 0:
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
    query = f"SELECT * FROM dbo.exercises\
                WHERE name='{name}'"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()

    if exercise == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise {name} is not found in the list of exercises",
        )

    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.post("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def addExerciseTO(exerciseTO: ExerciseTO):
    if type(searchExerciseTO("id", exerciseTO.id)) == ExerciseTO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The exercise with id = {exerciseTO.id} already exists",
        )

    query = f"INSERT dbo.exercises (creator, name, description)\
                OUTPUT INSERTED.*\
                VALUES ('{exerciseTO.creator}', '{exerciseTO.name}', '{exerciseTO.description}')"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.put("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def updateExerciseTO(exercise: ExerciseTO):
    exercise_search = searchExerciseTO("id", exercise.id)
    if type(exercise_search) != ExerciseTO:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exercise_search["error"]
        )

    query = f"UPDATE dbo.exercises\
                SET creator = '{exercise.creator}', name = '{exercise.name}', description = '{exercise.description}'\
                OUTPUT INSERTED.*\
                WHERE id={exercise.id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))


@router.delete("/{id}", response_model=ExerciseTO, status_code=status.HTTP_200_OK)
async def deleteExerciseTO(id: int):
    exercise_search = searchExerciseTO("id", id)
    if type(exercise_search) != ExerciseTO:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exercise_search["error"]
        )

    query = f"DELETE FROM dbo.relationRoutinesExercises\
                WHERE exerciseId={id}"
    sql_cursor.execute(query)

    query = f"DELETE FROM dbo.exercises\
                OUTPUT DELETED.*\
                WHERE id={id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
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
