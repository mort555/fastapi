from sqlalchemy.orm import Session

from app.core.filtering import FilterParams
from app.exceptions import (
    CategoryNotFoundError,
    DishNotFoundError,
    RestaurantNotFoundError,
)
from app.models.dish import Dish
from app.repositories.category import CategoryRepository
from app.repositories.dish import DishRepository
from app.repositories.restaurant import RestaurantRepository
from app.schemas.dish import DishCreate, DishUpdate


class DishService:
    def __init__(self, db: Session):
        self.repository = DishRepository(db)
        self.category_repository = CategoryRepository(db)
        self.restaurant_repository = RestaurantRepository(db)

    def _validate_category(
        self,
        category_id: int,
        restaurant_id: int,
    ) -> None:
        category = self.category_repository.get_by_id(
            category_id,
        )

        if category is None:
            raise CategoryNotFoundError()

        if category.restaurant_id != restaurant_id:
            raise CategoryNotFoundError()

    def _validate_restaurant(
        self,
        restaurant_id: int,
    ) -> None:
        restaurant = self.restaurant_repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            raise RestaurantNotFoundError()

    def get_all_by_restaurant(
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
    ):
        self._validate_restaurant(
            restaurant_id,
        )

        params = FilterParams(
            page=page,
            page_size=page_size,
        )

        dishes, total = (
            self.repository.get_filtered_by_restaurant(
                restaurant_id=restaurant_id,
                category_id=category_id,
                min_price=min_price,
                max_price=max_price,
                is_available=is_available,
                search=search,
                ordering=ordering,
                params=params,
            )
        )

        return {
            "items": dishes,
            "page": params.page,
            "page_size": params.page_size,
            "total": total,
            "pages": params.get_pages(total),
        }

    def get_by_id(
        self,
        dish_id: int,
    ) -> Dish:
        dish = self.repository.get_by_id(
            dish_id,
        )

        if dish is None:
            raise DishNotFoundError()

        return dish

    def create(
        self,
        restaurant_id: int,
        dish_data: DishCreate,
    ) -> Dish:
        self._validate_restaurant(
            restaurant_id,
        )

        self._validate_category(
            dish_data.category_id,
            restaurant_id,
        )

        dish = Dish(
            restaurant_id=restaurant_id,
            category_id=dish_data.category_id,
            name=dish_data.name,
            description=dish_data.description,
            price=dish_data.price,
            weight=dish_data.weight,
            is_available=dish_data.is_available,
        )

        return self.repository.create(
            dish,
        )

    def update(
        self,
        dish_id: int,
        dish_data: DishUpdate,
    ) -> Dish:
        dish = self.get_by_id(
            dish_id,
        )

        update_data = dish_data.model_dump(
            exclude_unset=True,
        )

        if "category_id" in update_data:
            self._validate_category(
                update_data["category_id"],
                dish.restaurant_id,
            )

        for field, value in update_data.items():
            setattr(
                dish,
                field,
                value,
            )

        return self.repository.update(
            dish,
        )

    def delete(
        self,
        dish_id: int,
    ) -> bool:
        dish = self.get_by_id(
            dish_id,
        )

        self.repository.delete(
            dish,
        )

        return True