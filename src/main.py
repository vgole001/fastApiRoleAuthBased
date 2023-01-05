from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import database, models, crud
import send_email
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
import uuid as uuid_pkg
import auth

app = FastAPI( title="Role Based Users Management System")

@app.on_event("startup")
async def startup_event():
    database.create_db_and_tables()
    
@app.post("/register")
def register_user(user: models.UserSchema, db: Session = Depends(database.get_db)):
    db_user_username = crud.get_user_by_username(db, username = user.username)
    db_user_email    = crud.get_user_by_email(db, email = user.email)
    if db_user_username or db_user_email:
        raise HTTPException(status_code=400, detail="Another user has the same email or username. Please choose a different one")
    db_user = crud.create_user(user=user, db=db)
    # db_user_id = crud.get_user_by_id(db, user_id = db_user_username.id)
    send_email.send_mail(to="vgoles@yahoo.com", first_name=user.first_name, last_name=user.last_name, role=user.role, user_id=4)
    return db_user

@app.post("/login")
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_username(db = db, username = form_data.username)
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Wrong credentials.")
    access_token = auth.create_access_token(db_user)
    refresh_token = auth.create_refresh_token(db_user)
    return {"access_token": access_token, "type": "Bearer", "refresh_token":refresh_token}

@app.post('/refresh', dependencies=[Depends(auth.check_active)])
def refresh(db: Session = Depends(database.get_db)):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    #db_user = crud.get_user_by_id(db, user_id)
    #Authorize: AuthJWT = Depends()
    # Authorize.jwt_refresh_token_required()

    # current_user = Authorize.get_jwt_subject()
    # print("Current user is ",current_user)
    # new_access_token = auth.create_access_token(subject=current_user)
    # new_access_token = auth.create_access_token(user)
    # print("db_user is",db_user)
    db_user = crud.get_user_by_username(db = db, username = "vuser001")
    # print("username is",user)
    access_token = auth.create_access_token(db_user)
    return {"access_token": access_token, "type": "Bearer"}

@app.post("/activate", dependencies=[Depends(auth.check_admin)], response_class=HTMLResponse)
def activate_user(user_id: uuid_pkg.UUID, db : Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user and not db_user.is_active:
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
        return f"""
            <html>
                <head>
                    <title>Activation Confirmation</title>
                </head>
                <body>
                    <h2>Account of {db_user.username} has been successfully activated.</h2>
                    <a href="https://google.com">
                        Return
                    </a>
                </body>
            </html>
        """
    elif db_user and db_user.is_active:
        return f"""
            <html>
                <head>
                    <title>Activation Confirmation</title>
                </head>
                <body>
                    <h2>Account of {db_user.username} is already activated.</h2>
                </body>
            </html>
        """
    else:
        raise HTTPException(status_code = 404, detail = "User not found. Please try a different user id.")

@app.get("/users")
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    return users

@app.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    print("dependencis at secure",auth.check_active())
    return users

@app.get("/secured/me")
def get_me(username: str = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db = db, username = username)
    return user

@app.get("/admins_only", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(database.get_db)):    
    users = crud.get_users(db = db)
    return users

@app.delete("/admins_only/delete_user", dependencies=[Depends(auth.check_admin)])
def delete_user_by_id(user_id: uuid_pkg.UUID, db: Session = Depends(database.get_db)):    
    return crud.delete_user_by_id(db, user_id)
    
