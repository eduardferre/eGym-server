from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from ddbb.sqlDB.client import sqlserver_client
from ddbb.sqlDB.models.userTO import UserTO
from ddbb.sqlDB.schemas.userTO import usersTO_schema, userTO_schema

sql_cursor = sqlserver_client.cursor()

sql_cursor.execute('SELECT * FROM dbo.users')
row = sql_cursor.fetchone()
while row:  
    print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))     
    row = sql_cursor.fetchone()