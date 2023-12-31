import os
import pymssql

if os.getenv("TEST_ENABLED") == "FALSE":
    sqlserver_client = pymssql.connect(
        server="localhost",
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD"),
        database="LocalDB",
    )
else:
    sqlserver_client = pymssql.connect(
        server="localhost",
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD"),
        database="TestDB",
        autocommit=False,
    )
