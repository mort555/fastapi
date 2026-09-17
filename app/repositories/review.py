from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Review]:
        return (
            self.db.query(Review)
            .filter(
                Review.restaurant_id == restaurant_id,
            )
            .order_by(Review.id)
            .all()
        )

    def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:
        return (
            self.db.query(Review)
            .filter(Review.id == review_id)
            .first()
        )

    def customer_has_order(
        self,
        customer_id: int,
        restaurant_id: int,
    ) -> bool:
        return (
            self.db.query(Order)
            .filter(
                Order.customer_id == customer_id,
                Order.restaurant_id == restaurant_id,
            )
            .first()
            is not None
        )

    def create(
        self,
        review: Review,
    ) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    def delete(
        self,
        review: Review,
    ) -> None:
        self.db.delete(review)
        self.db.commit()