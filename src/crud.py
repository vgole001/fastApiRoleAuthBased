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

def get_user_by_id(db: Session, id: str):
    user = db.query(models_and_schemas.User).filter(models_and_schemas.User.id == id).first()
    if user is not None:
        return user
    return False

def delete_user_by_id(db: Session, user_id):
    if get_user_by_id(db, user_id):
       db.query(models_and_schemas.User).filter_by(id = user_id).delete()
       db.commit()
       return f"User with id {user_id} successfully deleted."
    return f"User with {user_id} does not exist!"
