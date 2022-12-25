from sqlmodel import SQLModel, Field
from fastapi import Query, Body
from pydantic import EmailStr, validator, ValidationError
from enum import Enum
from typing import Optional, Union
from datetime import datetime, timezone
import re
from dotenv import load_dotenv
import os


class Roles(str, Enum):
    user    = "user"
    admin   = "admin"
    
class BaseUser(SQLModel):
    email       : EmailStr
    username    : Optional[str] = None
    is_active   : bool = False
    role        : Roles = "user"
    created_at  : datetime = Field(default=datetime.utcnow(), nullable=False)
    
    @validator('username')
    def username_validator(cls, v):
        if not re.match("^([a-zA-Z0-9_.-]).{5,}$", v) or v.isdigit():
            raise ValueError("Username must be at least 5 alphanumeric characters")
        return v
     
class User(BaseUser, table = True):
    # primary key for the table
    id : Optional[int] = Field(default=None,  primary_key=True)
    hashed_password : str
    __table_args__ = {'schema': os.environ["POSTGRES_SCHEMA"]}

class UserSchema(BaseUser):
    password: str
    
    @validator('password') 
    def password_validator(cls, v):
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-+]).{6,}$", v):
            raise ValueError("Password must contain minimum 6 charactes at least one upper case letter one lower case letter one digit and one special character ")
        return v.title()