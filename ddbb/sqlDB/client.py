import pymssql
import environment_variables

conn = pymssql.connect(server='localhost', user=environment_variables.SQL_USER, password=environment_variables.SQL_PASSWORD, database='TestDB')