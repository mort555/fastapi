import math

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.dish import Dish
from app.repositories.dish import DishRepository
from app.schemas.dish import DishCreate, DishUpdate


class DishService:
    def __init__(self, db: Session):
        self.repository = DishRepository(db)
        self.db = db

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
    ) -> dict:

        dishes, total = self.repository.get_filtered_by_restaurant(
            restaurant_id=restaurant_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            is_available=is_available,
            search=search,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )

        pages = math.ceil(total / page_size) if total else 0

        return {
            "items": dishes,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": pages,
        }

    def get_by_id(
        self,
        dish_id: int,
    ) -> Dish | None:
        return self.repository.get_by_id(dish_id)

    def create(
        self,
        restaurant_id: int,
        dish_data: DishCreate,
    ) -> Dish | None:

        category = (
            self.db.query(Category)
            .filter(
                Category.id == dish_data.category_id,
                Category.restaurant_id == restaurant_id,
            )
            .first()
        )

        if category is None:
            return None

        dish = Dish(
            restaurant_id=restaurant_id,
            category_id=dish_data.category_id,
            name=dish_data.name,
            description=dish_data.description,
            price=dish_data.price,
            weight=dish_data.weight,
            is_available=True,
        )

        return self.repository.create(dish)

    def update(
        self,
        dish_id: int,
        dish_data: DishUpdate,
    ) -> Dish | None:

        dish = self.repository.get_by_id(dish_id)

        if dish is None:
            return None

        update_data = dish_data.model_dump(
            exclude_unset=True,
        )

        if "category_id" in update_data:
            category = (
                self.db.query(Category)
                .filter(
                    Category.id == update_data["category_id"],
                    Category.restaurant_id == dish.restaurant_id,
                )
                .first()
            )

            if category is None:
                return None

        for field, value in update_data.items():
            setattr(dish, field, value)

        return self.repository.update(dish)

    def delete(
        self,
        dish_id: int,
    ) -> bool:

        dish = self.repository.get_by_id(dish_id)

        if dish is None:
            return False

        self.repository.delete(dish)

        return True