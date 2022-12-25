from passlib.context import CryptContext
import models_and_schemas
from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET = "asecretkey"
ALGORITHM  = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models_and_schemas.User):
    claims = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=120)
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)