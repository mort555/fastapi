from sqlalchemy.orm import Session

from app.core.filtering import FilterParams
from app.exceptions import (
    InvalidDateRangeError,
    RestaurantNotFoundError,
)
from app.models.restaurant import Restaurant
from app.repositories.restaurant import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    def __init__(self, db: Session):
        self.repository = RestaurantRepository(db)

    def get_filtered(
        self,
        search: str | None = None,
        is_active: bool | None = None,
        min_rating: float | None = None,
        ordering: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        params = FilterParams(
            page=page,
            page_size=page_size,
        )

        rows, total = self.repository.get_filtered(
            search=search,
            is_active=is_active,
            min_rating=min_rating,
            ordering=ordering,
            params=params,
        )

        items = []

        for restaurant, rating, reviews_count in rows:
            restaurant.rating = rating
            restaurant.reviews_count = reviews_count
            items.append(restaurant)

        return {
            "items": items,
            "page": params.page,
            "page_size": params.page_size,
            "total": total,
            "pages": params.get_pages(total),
        }

    def get_by_id(
        self,
        restaurant_id: int,
    ) -> Restaurant:
        restaurant = self.repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            raise RestaurantNotFoundError()

        return restaurant

    def get_statistics(
        self,
        restaurant_id: int,
    ):
        self.get_by_id(restaurant_id)

        return self.repository.get_statistics(
            restaurant_id,
        )

    def get_sales(
        self,
        restaurant_id: int,
        date_from,
        date_to,
    ):
        self.get_by_id(restaurant_id)

        if date_from > date_to:
            raise InvalidDateRangeError()

        sales = self.repository.get_sales(
            restaurant_id,
            date_from,
            date_to,
        )

        return {
            "date_from": date_from,
            "date_to": date_to,
            **sales,
        }

    def create(
        self,
        restaurant_data: RestaurantCreate,
    ) -> Restaurant:
        restaurant = Restaurant(
            name=restaurant_data.name,
            description=restaurant_data.description,
            address=restaurant_data.address,
            phone=restaurant_data.phone,
        )

        return self.repository.create(restaurant)

    def update(
        self,
        restaurant_id: int,
        restaurant_data: RestaurantUpdate,
    ) -> Restaurant:
        restaurant = self.get_by_id(
            restaurant_id,
        )

        update_data = restaurant_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(restaurant, field, value)

        return self.repository.update(restaurant)

    def delete(
        self,
        restaurant_id: int,
    ) -> bool:
        restaurant = self.get_by_id(
            restaurant_id,
        )

        self.repository.delete(restaurant)

        return True