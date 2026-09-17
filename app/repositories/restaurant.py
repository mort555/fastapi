from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant
from app.models.review import Review


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        restaurant_id: int,
    ) -> Restaurant | None:
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )

    def get_filtered(
        self,
        search: str | None = None,
        is_active: bool | None = None,
        min_rating: float | None = None,
        ordering: str | None = None,
        page: int = 1,
        page_size: int = 10,
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

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                Restaurant.name.ilike(search_pattern),
            )

        if is_active is not None:
            query = query.filter(
                Restaurant.is_active == is_active,
            )

        if min_rating is not None:
            query = query.filter(
                func.coalesce(
                    review_stats.c.rating,
                    0,
                ) >= min_rating,
            )

        total = query.count()

        if ordering:
            descending = ordering.startswith("-")
            field_name = ordering.lstrip("-")

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

            field = allowed_fields.get(field_name)

            if field is not None:
                if descending:
                    query = query.order_by(field.desc())
                else:
                    query = query.order_by(field.asc())
        else:
            query = query.order_by(Restaurant.id)

        offset = (page - 1) * page_size

        rows = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return rows, total

    def get_statistics(
        self,
        restaurant_id: int,
    ):
        orders_count = (
            self.db.query(func.count(Order.id))
            .filter(
                Order.restaurant_id == restaurant_id,
            )
            .scalar()
            or 0
        )

        total_sales = (
            self.db.query(
                func.coalesce(
                    func.sum(Order.total_price),
                    0,
                ),
            )
            .filter(
                Order.restaurant_id == restaurant_id,
            )
            .scalar()
        )

        average_order_price = (
            self.db.query(
                func.coalesce(
                    func.avg(Order.total_price),
                    0,
                ),
            )
            .filter(
                Order.restaurant_id == restaurant_id,
            )
            .scalar()
        )

        top_dishes = (
            self.db.query(
                Dish.id.label("dish_id"),
                Dish.name.label("dish_name"),
                func.sum(
                    OrderItem.quantity,
                ).label("quantity"),
                func.sum(
                    OrderItem.quantity * OrderItem.price,
                ).label("sales"),
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
            )
            .group_by(
                Dish.id,
                Dish.name,
            )
            .order_by(
                func.sum(
                    OrderItem.quantity,
                ).desc(),
            )
            .limit(10)
            .all()
        )

        return {
            "orders_count": orders_count,
            "total_sales": total_sales,
            "average_order_price": average_order_price,
            "top_dishes": top_dishes,
        }

    def get_sales(
        self,
        restaurant_id: int,
        date_from,
        date_to,
    ):
        orders_query = (
            self.db.query(Order)
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.created_at >= date_from,
                Order.created_at <= date_to,
            )
        )

        orders_count = orders_query.count()

        total_sales = (
            orders_query.with_entities(
                func.coalesce(
                    func.sum(Order.total_price),
                    0,
                ),
            )
            .scalar()
        )

        return {
            "orders_count": orders_count,
            "total_sales": total_sales,
        }

    def create(
        self,
        restaurant: Restaurant,
    ) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    def update(
        self,
        restaurant: Restaurant,
    ) -> Restaurant:
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    def delete(
        self,
        restaurant: Restaurant,
    ) -> None:
        self.db.delete(restaurant)
        self.db.commit()