from sqlmodel import Session
from auth import create_password_hash
import models_and_schemas

def create_user(db: Session, user: models_and_schemas.UserSchema):
    db_user = models_and_schemas.User(
        email           = user.email,
        username        = user.username,
        role            = user.role.value,
        created_at      = user.created_at,
        hashed_password = create_password_hash(user.password)
    )
    print("user before added into db",db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    users = db.query(models_and_schemas.User).all()
    return users

def get_user_by_username(db: Session, username: str):
    return (db.query(models_and_schemas.User).filter(models_and_schemas.User.username == username).first())

def get_user_by_email(db: Session, email: str):
    return (db.query(models_and_schemas.User).filter(models_and_schemas.User.email == email).first())
