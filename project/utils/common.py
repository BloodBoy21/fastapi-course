import jwt
from datetime import datetime, timedelta
from project.database import User
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

SECRET_KEY = os.getenv("SECRET_KEY")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")


def create_access_token(user: User, days=7) -> str:
    data = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=days),
    }
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    data = decode_access_token(token)
    if data is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User.select().where(User.id == data["user_id"]).first()
    return user
