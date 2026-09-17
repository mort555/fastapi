from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.review import ReviewRepository
from app.schemas.review import ReviewCreate


class ReviewService:
    def __init__(self, db: Session):
        self.repository = ReviewRepository(db)

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Review]:
        return self.repository.get_all_by_restaurant(
            restaurant_id,
        )

    def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:
        return self.repository.get_by_id(review_id)

    def create(
        self,
        review_data: ReviewCreate,
    ) -> Review:

        has_order = self.repository.customer_has_order(
            customer_id=review_data.customer_id,
            restaurant_id=review_data.restaurant_id,
        )

        if not has_order:
            raise ValueError(
                "Customer has no orders in this restaurant",
            )

        review = Review(
            customer_id=review_data.customer_id,
            restaurant_id=review_data.restaurant_id,
            rating=review_data.rating,
            text=review_data.text,
        )

        return self.repository.create(review)

    def delete(
        self,
        review_id: int,
    ) -> bool:
        review = self.repository.get_by_id(review_id)

        if review is None:
            return False

        self.repository.delete(review)

        return True