"""
This file contains the configurations for the FastAPI app.
"""

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from wait_for_db import wait_for_db
from database import SessionLocal, engine
from user import models
from os import getenv


# JWT CONFIG
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# Wait for the database to be ready
wait_for_db()

# SWAGGER CONFIG
SWAGGER_UI_PARAMETERS = {
    'deepLinking': True,
}

SWAGGER_UI_INIT_OAUTH = {
    "clientId": "",
    "clientSecret": "",
    "realm": "Stocks API",
    "appName": "Stocks API",
    "scopeSeparator": " ",
    "scopes": "read write",
    "useBasicAuthenticationWithAccessCodeGrant": True
}

# OAUTH2 CONFIG
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

# FastAPI app
app = FastAPI(swagger_ui_parameters=SWAGGER_UI_PARAMETERS, swagger_ui_init_oauth=SWAGGER_UI_INIT_OAUTH,
              title="Stocks API",
              description="API for stocks management",
              openapi_schema=oauth2_scheme)

# CORS CONFIG
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()