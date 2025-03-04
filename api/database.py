"""
This file contains the database configuration for the application.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DB"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()