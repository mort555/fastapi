from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.dish import Dish


class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        dish_id: int,
    ) -> Dish | None:
        return (
            self.db.query(Dish)
            .filter(Dish.id == dish_id)
            .first()
        )

    def get_filtered_by_restaurant(
        self,
        restaurant_id: int,
        category_id: int | None = None,
        min_price=None,
        max_price=None,
        is_available: bool | None = None,
        search: str | None = None,
        ordering: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[Dish], int]:

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

        # Считаем количество отдельно,
        # пока сортировка еще не применена.
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

        offset = (page - 1) * page_size

        dishes = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return dishes, total

    def create(
        self,
        dish: Dish,
    ) -> Dish:
        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)

        return dish

    def update(
        self,
        dish: Dish,
    ) -> Dish:
        self.db.commit()
        self.db.refresh(dish)

        return dish

    def delete(
        self,
        dish: Dish,
    ) -> None:
        self.db.delete(dish)
        self.db.commit()