import time

import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

from .config import settings
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

def connect_database():
    while True:
    #Try connection with Postgres Database
        try:
            conn = psycopg2.connect(host=settings.database_host, 
                                    database=settings.database_name,
                                    user=settings.database_user,
                                    password=settings.database_pwd,
                                    cursor_factory=RealDictCursor)
            print("Database connection was succesfull!")
            break
        except Exception as error:
            print("Connection failure")
            print(f"Error: {error}")
            time.sleep(3)
    return conn

conn = connect_database()

from .routes import items, users, auth

#Instanciating FastAPI
app = FastAPI()

#SET ORIGINS RELATED TO DOMAIN
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)
