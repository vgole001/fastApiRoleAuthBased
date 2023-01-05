from sqlmodel import SQLModel, Field
from sqlalchemy import MetaData
from fastapi import Query, Body
from pydantic import EmailStr, validator, ValidationError
from enum import Enum
from typing import Optional, Union
from datetime import datetime, timezone
from dotenv import load_dotenv
import uuid as uuid_pkg
import re
import os

meta = MetaData(schema="mySchema")

class Roles(str, Enum):
    user    = "user"
    admin   = "admin"
    
class BaseUser(SQLModel):
    email       : EmailStr
    first_name  : Optional[str] = None
    last_name   : Optional[str] = None
    username    : Optional[str] = None
    is_active   : bool = False
    role        : Optional[Roles] = "user"
    created_at  : datetime = Field(default=datetime.utcnow(), nullable=False)
    
    @validator("first_name")
    def first_name_validator(cls, v):
        if not re.match("^([a-zA-Z.-]).{3,}$", v) or v.isdigit():
            raise ValueError("First name must be at least 3 characters")
        return v
    
    @validator("last_name")
    def last_name_validator(cls, v):
        if not re.match("^([a-zA-Z.-]).{3,}$", v) or v.isdigit():
            raise ValueError("Last name must be at least 3 characters")
        return v
    
    @validator("username")
    def username_validator(cls, value):
        if not re.match("^([a-zA-Z0-9_.-]).{5,}$", value) or value.isdigit():
            raise ValueError("Username must be at least 5 alphanumeric characters")
        return value
     
# class name is reflected as the table name in database in lowercase
class User(BaseUser, table = True):
    __table_args__ = {"schema": os.environ["POSTGRES_SCHEMA"]}
    # primary key for the table
    id :  Optional[uuid_pkg.UUID] = Field(default_factory=uuid_pkg.uuid1,  primary_key=True, index=True, nullable=False)
    hashed_password : str

class UserSchema(BaseUser):
    password: str
    
    @validator("password") 
    def password_validator(cls, value):
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&{}_;`:*-+]).{6,}$", value):
            raise ValueError("Password must contain minimum 6 charactes at least one upper case letter one lower case letter one digit and one special character ")
        return value