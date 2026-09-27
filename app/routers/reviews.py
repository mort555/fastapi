from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review import ReviewService


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "",
    response_model=ReviewResponse,
)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.create(
        review_data,
    )


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[ReviewResponse],
)
def get_restaurant_reviews(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.get_all_by_restaurant(
        restaurant_id,
    )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.get_by_id(
        review_id,
    )


@router.delete(
    "/{review_id}",
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    service.delete(
        review_id,
    )

    return {
        "message": "Review deleted successfully",
    }