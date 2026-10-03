from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.filtering import DishFilterParams, FilterMixin
from app.models.dish import Dish
from app.repositories.base import BaseRepository


class DishRepository(
    BaseRepository[Dish],
    FilterMixin,
):
    model = Dish

    def __init__(self, db: Session):
        super().__init__(db)

    def get_filtered_by_restaurant(
        self,
        restaurant_id: int,
        params: DishFilterParams,
    ) -> tuple[list[Dish], int]:
        query = self.db.query(Dish).filter(
            Dish.restaurant_id == restaurant_id,
        )

        if params.category_id is not None:
            query = query.filter(
                Dish.category_id == params.category_id,
            )

        if params.min_price is not None:
            query = query.filter(
                Dish.price >= params.min_price,
            )

        if params.max_price is not None:
            query = query.filter(
                Dish.price <= params.max_price,
            )

        if params.is_available is not None:
            query = query.filter(
                Dish.is_available == params.is_available,
            )

        query = self.apply_search(
            query,
            Dish.name,
            params.search,
        )

        total = query.with_entities(
            func.count(Dish.id),
        ).scalar() or 0

        allowed_fields = {
            "name": Dish.name,
            "price": Dish.price,
            "weight": Dish.weight,
            "created_at": Dish.created_at,
        }

        query = self.apply_ordering(
            query,
            params.ordering,
            allowed_fields,
            Dish.id,
        )

        return self.paginate(
            query,
            params,
        )