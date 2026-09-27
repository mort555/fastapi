from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.filtering import FilterParams
from app.models.dish import Dish
from app.repositories.base import BaseRepository


class DishRepository(BaseRepository[Dish]):
    model = Dish

    def __init__(self, db: Session):
        super().__init__(db)

    def get_filtered_by_restaurant(
        self,
        restaurant_id: int,
        category_id: int | None = None,
        min_price=None,
        max_price=None,
        is_available: bool | None = None,
        search: str | None = None,
        ordering: str | None = None,
        params: FilterParams | None = None,
    ) -> tuple[list[Dish], int]:
        if params is None:
            params = FilterParams()

        query = self.db.query(Dish).filter(
            Dish.restaurant_id == restaurant_id,
        )

        if category_id is not None:
            query = query.filter(
                Dish.category_id == category_id,
            )

        if min_price is not None:
            query = query.filter(
                Dish.price >= min_price,
            )

        if max_price is not None:
            query = query.filter(
                Dish.price <= max_price,
            )

        if is_available is not None:
            query = query.filter(
                Dish.is_available == is_available,
            )

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                Dish.name.ilike(search_pattern),
            )

        total = query.with_entities(
            func.count(Dish.id),
        ).scalar() or 0

        if ordering:
            descending = ordering.startswith("-")
            field_name = ordering.lstrip("-")

            allowed_fields = {
                "name": Dish.name,
                "price": Dish.price,
                "weight": Dish.weight,
                "created_at": Dish.created_at,
            }

            field = allowed_fields.get(field_name)

            if field is not None:
                if descending:
                    query = query.order_by(field.desc())
                else:
                    query = query.order_by(field.asc())
        else:
            query = query.order_by(Dish.id)

        dishes = (
            query
            .offset(params.offset)
            .limit(params.page_size)
            .all()
        )

        return dishes, total