from fastapi import APIRouter, HTTPException, status

from ddbb.sqlDB.client import sqlserver_client
from ddbb.sqlDB.models.exerciseTO import ExerciseTO
from ddbb.sqlDB.schemas.exerciseTO import exerciseTO_schema, exercisesTO_schema

sql_cursor = sqlserver_client.cursor()

router = APIRouter(prefix="/exercisesTO",
                   tags=["exercisesTO"],
                   responses={ status.HTTP_404_NOT_FOUND: { "message": "Not found" } })

@router.get("/", response_model=list[ExerciseTO], status_code=status.HTTP_200_OK)
async def getExercisesTO():
    query = f"SELECT * FROM dbo.exercises"
    sql_cursor.execute(query)
    exercises_list = list()
    exercise = sql_cursor.fetchone()
    
    if exercise == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="There are no exercises in the database")
    
    while exercise:
        exercises_list.append(ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise))))
        exercise = sql_cursor.fetchone()
    return exercises_list

@router.get("/{id}", response_model=ExerciseTO, status_code=status.HTTP_200_OK)
async def getExerciseTOById(id: int):
    query = f"SELECT * FROM dbo.exercises\
                WHERE id={id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    
    if exercise == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The exercise with id = {id} is not found")
    
    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))

@router.post("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def addExerciseTO(exerciseTO: ExerciseTO):
    if type(searchExerciseTO("name", exerciseTO.name)) == ExerciseTO:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"The exercise = {exerciseTO.name} already exists")
    
    query = f"INSERT dbo.exercises (creator, name, description)\
                OUTPUT INSERTED.*\
                VALUES ('{exerciseTO.creator}', '{exerciseTO.name}', '{exerciseTO.description}')"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))

@router.put("/", response_model=ExerciseTO, status_code=status.HTTP_201_CREATED)
async def updateExerciseTO(exercises_list: list[ExerciseTO]):
    exerciseTO_original, exerciseTO_update = exercises_list[0], exercises_list[1]
    exercise_search = searchExerciseTO("name", exerciseTO_original.name)
    if type(exercise_search) != ExerciseTO:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exercise_search["error"])
    
    query = f"UPDATE dbo.exercises\
                SET creator = '{exerciseTO_update.creator}', name = '{exerciseTO_update.name}', description = '{exerciseTO_update.description}'\
                OUTPUT INSERTED.*\
                WHERE id={exercise_search.id}"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
    sqlserver_client.commit()
    return ExerciseTO(**exerciseTO_schema(tupleExerciseTOToDict(exercise)))

@router.delete("/{name}", response_model=ExerciseTO, status_code=status.HTTP_200_OK)
async def deleteExerciseTO(name: str):
    exercise_search = searchExerciseTO("name", name)
    if type(exercise_search) != ExerciseTO:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exercise_search["error"])
    
    query = f"DELETE FROM dbo.exercises\
                OUTPUT DELETED.*\
                WHERE name='{name}'"
    sql_cursor.execute(query)
    exercise = sql_cursor.fetchone()
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
        return { "error": f"The exercise with {field} = '{key}' does not exist"}
    
def tupleExerciseTOToDict(exercise: dict):
    exercise_dict = dict({
        "_id": str(exercise[0]),
        "creator": exercise[1],
        "name": exercise[2],
        "description": exercise[3]
    })
    return(exercise_dict)