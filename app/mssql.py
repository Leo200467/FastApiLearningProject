import pyodbc

server = r"DESKTOP-SQJFVVC\\NEW_LOCALHOST"
database = "fastapi"
username = 'Leonardo'
password = ''

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER='+server+';\
                        DATABASE='+database+';\
                        UID='+username+';\
                        PWD='+ password)
cursor = cnxn.cursor()