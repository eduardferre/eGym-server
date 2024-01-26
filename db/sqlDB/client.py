import os
import pymssql
import logging

if os.getenv("TEST_ENABLED") == "FALSE":
    logging.info("SQLSERVER: Local eGym database running")
    sqlserver_client = pymssql.connect(
        server="localhost",
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD"),
        database="LocalDB",
    )
else:
    logging.info("SQLSERVER: Local eGym database running")
    sqlserver_client = pymssql.connect(
        server="localhost",
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD"),
        database="TestDB",
        autocommit=False,
    )
