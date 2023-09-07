import logging
from fastapi import APIRouter, HTTPException, status

from ddbb.sqlDB.client import sqlserver_client
from ddbb.sqlDB.models.userTO import UserTO
from ddbb.sqlDB.schemas.userTO import userTO_schema, usersTO_schema


sql_cursor = sqlserver_client.cursor()

router = APIRouter(
    prefix="/usersTO",
    tags=["usersTO"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}},
)


@router.get("/", response_model=list[UserTO], status_code=status.HTTP_200_OK)
async def getUsersTO():  # NOSONAR
    query = f"SELECT * FROM dbo.users"  # NOSONAR
    sql_cursor.execute(query)
    users_list = list()
    user = sql_cursor.fetchone()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="There are no users in the database",
        )

    while user:
        users_list.append(UserTO(**userTO_schema(tupleUserTOToDict(user))))
        user = sql_cursor.fetchone()
    return users_list


@router.get("/{id}", response_model=UserTO, status_code=status.HTTP_200_OK)
async def getUserTOById(id: int):  # NOSONAR
    query = f"SELECT * FROM dbo.users\
                WHERE id={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id = {id} is not found",
        )

    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.post("/", response_model=UserTO, status_code=status.HTTP_201_CREATED)
async def addUserTO(userTO: UserTO):
    if type(searchUserTO("id", userTO.id)) == UserTO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with id = {userTO.id} already exists",
        )

    query = f"INSERT dbo.users (username, firstName, lastName, email, password, birthDate)\
                OUTPUT INSERTED.*\
                VALUES ('{userTO.username}', '{userTO.firstname}', '{userTO.lastname}', '{userTO.email}', '{userTO.password}', '{userTO.birthDate}')"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.put("/", response_model=UserTO, status_code=status.HTTP_201_CREATED)
async def updateUserTO(user: UserTO):
    user_search = searchUserTO("id", user.id)
    if type(user_search) != UserTO:
        logging.info(user_search["error"])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_search["error"]
        )

    if user.username == user_search.username:
        logging.info(f"The username '{user.username}' is already used")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The username '{user.username} is already used",
        )

    query = f"UPDATE dbo.users\
                SET username = '{user.username}', firstName = '{user.firstname}', lastName = '{user.lastname}', email = '{user.email}', password = '{user.password}', birthDate = '{user.birthDate}'\
                OUTPUT INSERTED.*\
                WHERE id={user.id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()
    return UserTO(**userTO_schema(tupleUserTOToDict(user)))


@router.delete("/{id}", response_model=UserTO, status_code=status.HTTP_200_OK)
async def deleteUserTO(id: int):
    user_search = searchUserTO("id", id)
    if type(user_search) != UserTO:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=user_search["error"]
        )

    query = f"DELETE FROM dbo.users\
                OUTPUT DELETED.*\
                WHERE id={id}"
    sql_cursor.execute(query)
    user = sql_cursor.fetchone()
    sqlserver_client.commit()
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
