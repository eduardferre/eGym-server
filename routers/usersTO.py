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
    return usersTO_schema(sqlserver_client)