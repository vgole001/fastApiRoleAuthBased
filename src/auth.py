from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import models_and_schemas
import auth
from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET = "asecretkey"
ALGORITHM  = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models_and_schemas.User):
    claims = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=100)
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token):
    claims = jwt.decode(token, key = JWT_SECRET)
    return claims

def check_active(token: str = Depends(auth.oauth_scheme)):
    try:
        claims = decode_token(token)
        print("token is",token)
        if claims.get("is_active"):
            return claims
        raise HTTPException(
            status_code=401,
            detail="Please activate the account",
            headers={"WWW-Authenticate":"Bearer"}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=400,
            detail="Token has expired. Please login to refresh token.",
            headers={"WWW-Authenticate":"Bearer"}
        ) 
           
def check_admin(claims: dict = Depends(check_active)):  
    role = claims.get("role")
    # print("decode token claims",claims)
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return claims