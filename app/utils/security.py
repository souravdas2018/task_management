from passlib.context import CryptContext
from flask_jwt_extended import create_access_token
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_jwt_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(hours=1))
