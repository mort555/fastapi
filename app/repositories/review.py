from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.review import Review
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    model = Review

    def __init__(self, db: Session):
        super().__init__(db)

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