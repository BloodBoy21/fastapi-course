from fastapi import APIRouter
from .users import router as user_router
from .reviews import router as review_router

router = APIRouter(prefix="/api/v1")

router.include_router(user_router, tags=["users"], prefix="/users")
router.include_router(review_router, tags=["reviews"], prefix="/reviews")
