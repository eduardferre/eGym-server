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
    while user:
        user_dict = dict({
            "_id": str(user[0]),
            "username": user[1],
            "firstname": user[2],
            "lastname": user[3],
            "email": user[4],
            "password": user[5],
            "birthDate": str(user[6])
        })
        users_list.append(user_dict)
        user = sql_cursor.fetchone()
    return usersTO_schema(users_list)

@router.get("/{id}", response_model=UserTO)
async def getUserTOById(id: int): #NOSONAR
    query = f"SELECT * FROM dbo.users WHERE userId={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    user_dict = dict({
        "_id": str(user[0]),
        "username": user[1],
        "firstname": user[2],
        "lastname": user[3],
        "email": user[4],
        "password": user[5],
        "birthDate": str(user[6])
    })
    return userTO_schema(user_dict)