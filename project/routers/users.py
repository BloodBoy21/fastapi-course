from fastapi import APIRouter, HTTPException, Response, Cookie, Depends
from project.database import User
from project.schemas import UserRequestModel, UserResponseModel, ReviewResponseModel
from fastapi.security import HTTPBasicCredentials
from project.utils import common

router = APIRouter()


@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel) -> UserResponseModel:
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(status_code=409, detail="Username al ready exists")
    hash_password = User.create_password(user.password)
    user = User.create(username=user.username, password=hash_password)
    return user


@router.post("/login", response_model=UserResponseModel)
async def login_user(
    credentials: HTTPBasicCredentials, response: Response
) -> UserResponseModel:
    user = User.select().where(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    hash_password = User.create_password(credentials.password)
    if hash_password != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    response.set_cookie(key="user_id", value=user.id)
    return user


@router.get("/reviews", response_model=list[ReviewResponseModel])
async def get_user_reviews(
    user: User = Depends(common.get_current_user),
) -> list[ReviewResponseModel]:
    return user.reviews
