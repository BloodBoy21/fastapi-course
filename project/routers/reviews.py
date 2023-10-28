from fastapi import APIRouter, HTTPException
from project.database import User, Movie, UserReview
from project.schemas import (
    ReviewRequestModel,
    ReviewResponseModel,
    ReviewRequestPutModel,
)

router = APIRouter()


@router.post("", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel) -> ReviewResponseModel:
    if User().select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    if Movie().select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score,
    )
    return user_review


@router.get("", response_model=list[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10) -> list[ReviewResponseModel]:
    reviews = UserReview().select().paginate(page, limit)
    return reviews


@router.get("/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int) -> ReviewResponseModel:
    review = UserReview().select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}", response_model=ReviewResponseModel)
async def update_review(
    review_id: int, review: ReviewRequestPutModel
) -> ReviewResponseModel:
    review = UserReview().select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    review.review = review.review
    review.score = review.score
    review.save()
    return review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int) -> ReviewResponseModel:
    review = UserReview().select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    review.delete_instance()
    return review
