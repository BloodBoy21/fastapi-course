from fastapi import APIRouter, HTTPException, Depends
from project.database import User, Movie, UserReview
from project.schemas import (
    ReviewRequestModel,
    ReviewResponseModel,
    ReviewRequestPutModel,
)
from project.utils import common

router = APIRouter()


@router.post("", response_model=ReviewResponseModel)
async def create_review(
    user_review: ReviewRequestModel, user: User = Depends(common.get_current_user)
) -> ReviewResponseModel:
    if Movie().select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id=user.id,
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
    review_id: int,
    review: ReviewRequestPutModel,
    user: User = Depends(common.get_current_user),
) -> ReviewResponseModel:
    review = UserReview().select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can't update this review")
    review.review = review.review
    review.score = review.score
    review.save()
    return review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(
    review_id: int, user: User = Depends(common.get_current_user)
) -> ReviewResponseModel:
    review = UserReview().select().where(UserReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can't delete this review")
    review.delete_instance()
    return review
