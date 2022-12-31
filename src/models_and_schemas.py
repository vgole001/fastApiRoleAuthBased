from sqlmodel import SQLModel, Field
from sqlalchemy import MetaData
from fastapi import Query, Body
from pydantic import EmailStr, validator, ValidationError
from enum import Enum
from typing import Optional, Union
from datetime import datetime, timezone
import re
from dotenv import load_dotenv
import os

meta = MetaData(schema="mySchema")

class Roles(str, Enum):
    user    = "user"
    admin   = "admin"
    
class BaseUser(SQLModel):
    email       : EmailStr
    username    : Optional[str] = None
    is_active   : bool = False
    role        : Optional[Roles] = "user"
    created_at  : datetime = Field(default=datetime.utcnow(), nullable=False)
    
    @validator('username')
    def username_validator(cls, v):
        if not re.match("^([a-zA-Z0-9_.-]).{5,}$", v) or v.isdigit():
            raise ValueError("Username must be at least 5 alphanumeric characters")
        return v
     
# class name is reflected as the table name in database in lowercase
class User(BaseUser, table = True):
    __table_args__ = {'schema': os.environ["POSTGRES_SCHEMA"]}
    # primary key for the table
    # default = None means that we do not set it, it does not mean that it is Null
    # since primary keys cannot be null
    id : Optional[int] = Field(default=None,  primary_key=True, )
    hashed_password : str

class UserSchema(BaseUser):
    password: str
    
    @validator('password') 
    def password_validator(cls, v):
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-+]).{6,}$", v):
            raise ValueError("Password must contain minimum 6 charactes at least one upper case letter one lower case letter one digit and one special character ")
        return v