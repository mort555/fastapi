from math import ceil

from sqlalchemy.orm import Session

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
        rows, total = self.repository.get_filtered(
            search=search,
            is_active=is_active,
            min_rating=min_rating,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )

        items = []

        for restaurant, rating, reviews_count in rows:
            restaurant.rating = rating
            restaurant.reviews_count = reviews_count
            items.append(restaurant)

        pages = ceil(total / page_size) if total else 0

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": pages,
        }

    def get_by_id(
        self,
        restaurant_id: int,
    ) -> Restaurant | None:
        return self.repository.get_by_id(restaurant_id)

    def get_statistics(
        self,
        restaurant_id: int,
    ):
        restaurant = self.repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            return None

        return self.repository.get_statistics(
            restaurant_id,
        )

    def get_sales(
        self,
        restaurant_id: int,
        date_from,
        date_to,
    ):
        restaurant = self.repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            return None

        if date_from > date_to:
            raise ValueError(
                "date_from must be earlier than date_to",
            )

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
    ) -> Restaurant | None:
        restaurant = self.repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            return None

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
        restaurant = self.repository.get_by_id(
            restaurant_id,
        )

        if restaurant is None:
            return False

        self.repository.delete(restaurant)

        return True