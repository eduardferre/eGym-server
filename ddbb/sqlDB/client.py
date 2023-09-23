import pymssql
from utils import environment

sqlserver_client = pymssql.connect(server='localhost', user=environment.SQL_USER, password=environment.SQL_PASSWORD, database='TestDB')