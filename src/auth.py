from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"])

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)