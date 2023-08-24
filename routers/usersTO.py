from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from ddbb.sqlDB.client import sqlserver_client
from ddbb.sqlDB.models.userTO import UserTO
from ddbb.sqlDB.schemas.userTO import userTO_schema, usersTO_schema


sql_cursor = sqlserver_client.cursor()

router = APIRouter(prefix="/usersTO",
                   tags=["usersTO"],
                   responses={status.HTTP_404_NOT_FOUND: { "message": "Not found" }})

@router.get("/", response_model=list[UserTO])
async def getUsersTO(): #NOSONAR
    query = f"SELECT * FROM dbo.users" #NOSONAR
    sql_cursor.execute(query)
    users_list = list()
    user = sql_cursor.fetchone()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users in the database")
    
    while user:
        users_list.append(UserTO(**userTO_schema(tupleUserTOToDict(user))))
        user = sql_cursor.fetchone()
    return users_list

@router.get("/{id}", response_model=UserTO)
async def getUserTOById(id: int): #NOSONAR
    query = f"SELECT * FROM dbo.users WHERE userId={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id = {id} is not found")
    
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))

@router.post("/", response_model=UserTO, status_code=201)
async def postUserTO(userTO: UserTO):
    if type(searchUserTO("username", userTO.username)) == UserTO:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with username = {userTO.username} already exists")
    
    query = f"INSERT dbo.users (username, firstName, lastName, email, password, birthDate)\
                OUTPUT INSERTED.*\
                VALUES ('{userTO.username}', '{userTO.firstname}', '{userTO.lastname}', '{userTO.email}', '{userTO.password}', '{userTO.birthDate}')"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))

@router.put("/", response_model=UserTO, status_code=201)
async def updateUserTO(user_list: list[UserTO]):
    userTO_original, userTO_update = user_list[0], user_list[1]
    user_search = searchUserTO("username", userTO_original.username)
    if type(user_search) != UserTO:
        raise HTTPException(status_code=404, detail=user_search["error"])
    
    query = f"UPDATE dbo.users\
                SET username = '{userTO_update.username}', firstName = '{userTO_update.firstname}', lastName = '{userTO_update.lastname}', email = '{userTO_update.email}', password = '{userTO_update.password}', birthDate = '{userTO_update.birthDate}'\
                OUTPUT INSERTED.*\
                WHERE userId={user_search.id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))

@router.delete("/{username}", response_model=UserTO, status_code=201)
async def deleteUserTO(username: str):
    user_search = searchUserTO("username", username)
    if type(user_search) != UserTO:
        raise HTTPException(status_code=404, detail=user_search["error"])
    
    query = f"DELETE FROM dbo.users\
                OUTPUT DELETED.*\
                WHERE username='{username}'"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


# Methods
def searchUserTO(field: str, key):
    query = f"SELECT * FROM dbo.users WHERE {field}='{key}'"
    try:
        sql_cursor.execute(query)
        user = sql_cursor.fetchone()
        return UserTO(**userTO_schema(tupleUserTOToDict(user)))
    except:
        return { "error": f"The user with {field} = '{key}' does not exist"}
    
def tupleUserTOToDict(user: dict):
    user_dict = dict({
        "_id": str(user[0]),
        "username": user[1],
        "firstname": user[2],
        "lastname": user[3],
        "email": user[4],
        "password": user[5],
        "birthDate": str(user[6])
    })
    return(user_dict)