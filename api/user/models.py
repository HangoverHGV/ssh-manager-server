"""
This file contains the User model.
"""

from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, event, Text
from sqlalchemy.orm import relationship
import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    config_file_path = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))



    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(self, password):
        self.hashed_password = pwd_context.hash(password)