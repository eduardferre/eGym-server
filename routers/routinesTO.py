from fastapi import APIRouter, HTTPException, status

from ddbb.sqlDB.client import sqlserver_client
from ddbb.sqlDB.models.exerciseTO import ExerciseTO
from ddbb.sqlDB.models.routineTO import RoutineTO
from ddbb.sqlDB.schemas.routineTO import routineTO_schema, routinesTO_schema
from routers.exercisesTO import tupleExerciseTOToDict, searchExerciseTO

sql_cursor = sqlserver_client.cursor()

router = APIRouter(prefix="/routinesTO",
                   tags=["routinesTO"],
                   responses={ status.HTTP_404_NOT_FOUND: { "message": "Not found" } })

@router.get("/", response_model=list[RoutineTO], status_code=status.HTTP_200_OK)
async def getRoutinesTO():
    query = f"SELECT * FROM dbo.routines"
    sql_cursor.execute(query)
    routines_list = list()
    routine = sql_cursor.fetchone()
    
    if routine == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="There are no routines in the database")
    
    while routine:
        routines_list.append(RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine))))
        routine = sql_cursor.fetchone()
    return routines_list

@router.get("/{id}", response_model=RoutineTO, status_code=status.HTTP_200_OK)
async def getRoutineTOById(id: int):
    query = f"SELECT * FROM dbo.routines\
                WHERE id={id}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    
    if routine == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The routine with id = {id} is not found")
    
    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))

@router.get("/{creator}", response_model=list[RoutineTO], status_code=status.HTTP_200_OK)
async def getRoutinesTOByCreator(creator: str):
    query = f"SELECT * FROM dbo.routines\
                WHERE creator={creator}"
    routines_list = list()
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    
    if routine == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no routines made by {creator}")
    
    while routine:
        routines_list.append(RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine))))
        routine = sql_cursor.fetchone()
    return routines_list

@router.get("/{name}", response_model=list[RoutineTO], status_code=status.HTTP_200_OK)
async def getRoutinesTOByName(name: str):
    query = f"SELECT * FROM dbo.routines\
                WHERE name={name}"
    routines_list = list()
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    
    if routine == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There are not any routine named: {name}")
    
    while routine:
        routines_list.append(RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine))))
        routine = sql_cursor.fetchone()
    return routines_list

@router.post("/", response_model=RoutineTO, status_code=status.HTTP_201_CREATED)
async def addRoutineTO(routineTO: RoutineTO):
    if type(searchRoutineTO("name", routineTO.name)) == RoutineTO:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"The routine = {routineTO.name} already exists")
    
    #! ELS EXERCISIS VAN PER ID !!!
    
    query = f"INSERT dbo.routines (creator, name, description, exercisesId)\
                OUTPUT INSERTED.*\
                VALUES ('{routineTO.creator}', '{routineTO.name}', '{routineTO.description}', '{routineTO.exercisesId})"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    sqlserver_client.commit()
    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))

@router.put("/", response_model=RoutineTO, status_code=status.HTTP_201_CREATED)
async def updateRoutineTO(routines_list: list[RoutineTO]):
    routineTO_original, routineTO_update = routines_list[0], routines_list[1]
    routine_search = searchRoutineTO("name", routineTO_original.name)
    if type(routine_search) != RoutineTO:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=routine_search["error"])
    
    query = f"UPDATE dbo.routines\
                SET creator = '{routineTO_update.creator}', name = '{routineTO_update.name}', description = '{routineTO_update.description}'\
                OUTPUT INSERTED.*\
                WHERE id={routine_search.id}"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
    sqlserver_client.commit()
    return RoutineTO(**routineTO_schema(tupleRoutineTOToDict(routine)))

@router.delete("/{name}", response_model=RoutineTO, status_code=status.HTTP_200_OK)
async def deleteRoutineTO(name: str):
    routine_search = searchRoutineTO("name", name)
    if type(routine_search) != RoutineTO:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=routine_search["error"])
    
    query = f"DELETE FROM dbo.routines\
                OUTPUT DELETED.*\
                WHERE name='{name}'"
    sql_cursor.execute(query)
    routine = sql_cursor.fetchone()
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
        return { "error": f"The routine with {field} = '{key}' does not exist"}
    
def tupleRoutineTOToDict(routine: dict):
    exercises_list = searchRoutineExercises(routine[0])
    
    routine_dict = dict({
        "_id": str(routine[0]),
        "creator": routine[1],
        "name": routine[2],
        "description": routine[3],
        "exercises": exercises_list
    })
    
    return(routine_dict)

def searchRoutineExercises(routineId: int):
    query = f"SELECT exerciseId FROM dbo.relationRoutinesExercises\
                WHERE routineId={routineId}"
    exercisesId_list = list()
    sql_cursor.execute(query)
    exerciseId = sql_cursor.fetchone()
    
    while exerciseId:
        exercisesId_list.append(exerciseId[0])
        exerciseId = sql_cursor.fetchone()
    
    exercises_list = list()
    
    for exerciseId in exercisesId_list:
        exercises_list.append(searchExerciseTO("id", exerciseId))
        
    return exercises_list