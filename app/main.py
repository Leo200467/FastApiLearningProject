from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine

from .routes import auth, items, users

# INSTANCIATING DATABASE
app = FastAPI()

# INITIALIZING DATABASE
models.Base.metadata.create_all(bind=engine)

# SET ORIGINS RELATED TO DOMAIN
origins = ["*"]

# MIDDLEWARE SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# INCLUDING ROUTES
app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)
