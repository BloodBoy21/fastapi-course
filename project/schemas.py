from pydantic import BaseModel, validator
from pydantic.v1.utils import GetterDict
from typing import Any
from peewee import ModelSelect


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError(
                "username must be at least 3 characters and at most 50 characters"
            )
        return username


class ResponseModel(BaseModel):
    class Config:
        from_attributes = True


class ReviewValidator(BaseModel):
    @classmethod
    @validator("score")
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError("score must be between 1 and 5")
        return score


class UserResponseModel(ResponseModel):
    id: int
    username: str


class ReviewRequestModel(ReviewValidator):
    movie_id: int
    review: str
    score: int


class MovieResponseModel(ResponseModel):
    id: int
    title: str


class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int


class ReviewRequestPutModel(ReviewValidator):
    review: str
    score: int
