from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import database, models_and_schemas, crud

app = FastAPI()

@app.on_event("startup")
def startup_event():
    database.create_db_and_tables()
    
@app.post("/register")
def register_user(user: models_and_schemas.UserSchema, db: Session = Depends(database.get_db)):
    db_user_username = crud.get_user_by_username(db, username = user.username)
    db_user_email    = crud.get_user_by_email(db, email = user.email)
    if db_user_username or db_user_email:
        raise HTTPException(status_code=400, detail="Email or Username already exists in database")
    db_user = crud.create_user(user=user, db=db)
    return db_user

@app.get("/users")
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db=db)
    return users