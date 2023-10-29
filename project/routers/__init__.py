from fastapi import APIRouter, Depends, HTTPException
from .users import router as user_router
from .reviews import router as review_router
from fastapi.security import OAuth2PasswordRequestForm
from project.database import User
from project.utils import common

router = APIRouter(prefix="/api/v1")

router.include_router(user_router, tags=["users"], prefix="/users")
router.include_router(review_router, tags=["reviews"], prefix="/reviews")


@router.post("/auth", tags=["auth"])
async def auth(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = User.authenticate(data.username, data.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": common.create_access_token(user),
        "token_type": "Bearer",
    }
