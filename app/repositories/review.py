from sqlalchemy.orm import Session

from app.core.filtering import FilterMixin, ReviewFilterParams
from app.models.order import Order
from app.models.review import Review
from app.repositories.base import BaseRepository


class ReviewRepository(
    BaseRepository[Review],
    FilterMixin,
):
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

    def get_filtered(
        self,
        params: ReviewFilterParams,
    ) -> tuple[list[Review], int]:
        query = self.db.query(Review)

        if params.restaurant_id is not None:
            query = query.filter(
                Review.restaurant_id == params.restaurant_id,
            )

        if params.customer_id is not None:
            query = query.filter(
                Review.customer_id == params.customer_id,
            )

        if params.min_rating is not None:
            query = query.filter(
                Review.rating >= params.min_rating,
            )

        if params.max_rating is not None:
            query = query.filter(
                Review.rating <= params.max_rating,
            )

        query = self.apply_search(
            query,
            Review.text,
            params.search,
        )

        allowed_fields = {
            "id": Review.id,
            "rating": Review.rating,
            "created_at": Review.created_at,
        }

        query = self.apply_ordering(
            query,
            params.ordering,
            allowed_fields,
            Review.id,
        )

        return self.paginate(
            query,
            params,
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