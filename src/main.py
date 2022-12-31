from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import database, models_and_schemas, crud
import send_email
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
import auth

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
    # db_user_id = crud.get_user_by_id(db, user_id = db_user_username.id)
    send_email.send_mail(to="vgoles@yahoo.com", username=user.username, user_id=4)
    return db_user

@app.post("/login")
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_username(db = db, username = form_data.username)
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Wrong credentials.")
    token = auth.create_access_token(db_user)
    return {"access_token": token, "type": "Bearer"}

@app.post("/activate/{user_id}")
def activate_user(user_id: str, db : Session = Depends(database.get_db)):
    claims = auth.decode_token(token)
    username = claims.get("username")
    # db_user = crud.get_user_by_id(db, user_id)
    print("db user is",db_user)
    # db_user = db.get_user_by_username(dd, username)
    #db_user.is_active = True
    #db.commit()
    #db.refresh(db_user)
    return {
            "status": "success",
            "message": "Account verified successfully"
    }
    # return f"""
    #     <html>
    #         <head>
    #             <title>Activation Confirmation</title>
    #         </head>
    #         <body>
    #             <h2>Activation of USER_NAME successfull!</h2>
    #             <a href="https://google.com">
    #                 Return
    #             </a>
    #         </body>
    #     </html>
    # """

@app.get("/users")
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    return users

@app.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    return users

@app.get("/admins_only", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    return users

@app.delete("/delete_user/{user_id}", dependencies=[Depends(auth.check_admin)])
def delete_user_by_id(user_id: int, db: Session = Depends(database.get_db)):    
    return crud.delete_user_by_id(db, user_id)
    