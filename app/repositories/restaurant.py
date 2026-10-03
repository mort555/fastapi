from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.filtering import FilterMixin, RestaurantFilterParams
from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.repositories.base import BaseRepository


class RestaurantRepository(
    BaseRepository[Restaurant],
    FilterMixin,
):
    model = Restaurant

    def __init__(self, db: Session):
        super().__init__(db)

    def get_filtered(
        self,
        params: RestaurantFilterParams,
    ):
        review_stats = (
            self.db.query(
                Review.restaurant_id.label("restaurant_id"),
                func.avg(Review.rating).label("rating"),
                func.count(Review.id).label("reviews_count"),
            )
            .group_by(Review.restaurant_id)
            .subquery()
        )

        query = (
            self.db.query(
                Restaurant,
                func.coalesce(
                    review_stats.c.rating,
                    0,
                ).label("rating"),
                func.coalesce(
                    review_stats.c.reviews_count,
                    0,
                ).label("reviews_count"),
            )
            .outerjoin(
                review_stats,
                Restaurant.id == review_stats.c.restaurant_id,
            )
        )

        query = self.apply_search(
            query,
            Restaurant.name,
            params.search,
        )

        query = self.apply_is_active(
            query,
            Restaurant.is_active,
            params.is_active,
        )

        if params.min_rating is not None:
            query = query.filter(
                func.coalesce(
                    review_stats.c.rating,
                    0,
                ) >= params.min_rating,
            )

        allowed_fields = {
            "name": Restaurant.name,
            "created_at": Restaurant.created_at,
            "rating": func.coalesce(
                review_stats.c.rating,
                0,
            ),
            "reviews_count": func.coalesce(
                review_stats.c.reviews_count,
                0,
            ),
        }

        query = self.apply_ordering(
            query,
            params.ordering,
            allowed_fields,
            Restaurant.id,
        )

        return self.paginate(
            query,
            params,
        )

    def _get_orders_count(
        self,
        restaurant_id: int,
    ) -> int:
        return (
            self.db.query(Order.id)
            .filter(
                Order.restaurant_id == restaurant_id,
            )
            .count()
        )

    def _get_completed_orders_count(
        self,
        restaurant_id: int,
    ) -> int:
        return (
            self.db.query(Order.id)
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.status == "completed",
            )
            .count()
        )

    def _get_cancelled_orders_count(
        self,
        restaurant_id: int,
    ) -> int:
        return (
            self.db.query(Order.id)
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.status == "cancelled",
            )
            .count()
        )

    def _get_revenue(
        self,
        restaurant_id: int,
    ):
        result = (
            self.db.query(
                func.coalesce(
                    func.sum(Order.total_price),
                    0,
                )
            )
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.status == "completed",
            )
            .scalar()
        )

        return result

    def _get_average_order_price(
        self,
        restaurant_id: int,
    ):
        return (
            self.db.query(
                func.coalesce(
                    func.avg(Order.total_price),
                    0,
                )
            )
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.status == "completed",
            )
            .scalar()
        )

    def _get_average_rating(
        self,
        restaurant_id: int,
    ):
        return (
            self.db.query(
                func.coalesce(
                    func.avg(Review.rating),
                    0,
                )
            )
            .filter(
                Review.restaurant_id == restaurant_id,
            )
            .scalar()
        )

    def get_statistics(
        self,
        restaurant_id: int,
    ):
        return {
            "orders_count": self._get_orders_count(
                restaurant_id,
            ),
            "completed_orders": self._get_completed_orders_count(
                restaurant_id,
            ),
            "cancelled_orders": self._get_cancelled_orders_count(
                restaurant_id,
            ),
            "revenue": self._get_revenue(
                restaurant_id,
            ),
            "average_order_price": self._get_average_order_price(
                restaurant_id,
            ),
            "average_rating": self._get_average_rating(
                restaurant_id,
            ),
        }

    def get_sales(
        self,
        restaurant_id: int,
        date_from,
        date_to,
    ):
        orders_query = self.db.query(Order).filter(
            Order.restaurant_id == restaurant_id,
            Order.created_at >= date_from,
            Order.created_at <= date_to,
        )

        orders_count = orders_query.count()

        revenue = (
            self.db.query(
                func.coalesce(
                    func.sum(Order.total_price),
                    0,
                )
            )
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.created_at >= date_from,
                Order.created_at <= date_to,
            )
            .scalar()
        )

        top_dishes = (
            self.db.query(
                Dish.id,
                Dish.name,
                func.sum(OrderItem.quantity).label("quantity"),
                func.sum(
                    OrderItem.quantity * OrderItem.price
                ).label("revenue"),
            )
            .join(
                OrderItem,
                OrderItem.dish_id == Dish.id,
            )
            .join(
                Order,
                Order.id == OrderItem.order_id,
            )
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.created_at >= date_from,
                Order.created_at <= date_to,
            )
            .group_by(
                Dish.id,
                Dish.name,
            )
            .order_by(
                func.sum(
                    OrderItem.quantity
                ).desc()
            )
            .limit(10)
            .all()
        )

        return {
            "orders": orders_count,
            "revenue": revenue,
            "top_dishes": top_dishes,
        }