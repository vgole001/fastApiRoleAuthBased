from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import models
import auth
from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET = "asecretkey"
ALGORITHM  = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models.User):
    claims = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)

def create_refresh_token(user: models.User):
    claims = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes= 1440) # 24 hours before expiration is 1440 minutes
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token):
    claims = jwt.decode(token, key = JWT_SECRET)
    return claims

def check_active(token: str = Depends(auth.oauth_scheme)):
    try:
        claims = decode_token(token)
        if claims.get("is_active"):
            return claims
        raise HTTPException(
            status_code=401,
            detail="Please activate the account",
            headers={"WWW-Authenticate":"Bearer"}
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token. Please login to refresh token.",
            headers={"WWW-Authenticate":"Bearer"}
        ) 
           
def check_admin(claims: dict = Depends(check_active)):  
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only",
            headers={"WWW-Authenticate":"Bearer"}
        )
    print("admin claims",claims)
    return claims

def get_current_user(claims: dict = Depends(check_active)):  
    username = claims.get("username")
    if username is not None:
        return username
    raise HTTPException(
            status_code=400,
            detail="Failed to get current user",
            headers={"WWW-Authenticate":"Bearer"}
        )