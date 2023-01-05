from fastapi import Depends
from sqlmodel import Session
from auth import create_password_hash
import models
import uuid as uuid_pkg

db_user = None

def create_user(db: Session, user: models.UserSchema):
    db_user = models.User(
        email           = user.email,
        first_name      = user.first_name,
        last_name       = user.last_name,
        username        = user.username,
        role            = user.role.value,
        created_at      = user.created_at,
        hashed_password = create_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    users = db.query(models.User).all()
    return users

def get_user_by_username(db: Session, username: str):
    return (db.query(models.User).filter(models.User.username == username).first())

def get_user_by_email(db: Session, email: str):
    return (db.query(models.User).filter(models.User.email == email).first())

def get_user_by_id(db: Session, id: uuid_pkg.UUID):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is not None:
        return user
    return False

def delete_user_by_id(db: Session, user_id):
    if get_user_by_id(db, user_id):
       db.query(models.User).filter_by(id = user_id).delete()
       db.commit()
       return f"User with id {user_id} successfully deleted."
    return f"User not found. Make sure you entered a valid user id."
