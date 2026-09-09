from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.repositories.restaurant import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    def __init__(self, db: Session):
        self.repository = RestaurantRepository(db)

    def get_all(self) -> list[Restaurant]:
        return self.repository.get_all()

    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        return self.repository.get_by_id(restaurant_id)

    def create(self, restaurant_data: RestaurantCreate) -> Restaurant:
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
        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            return None

        update_data = restaurant_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(restaurant, field, value)

        return self.repository.update(restaurant)

    def delete(self, restaurant_id: int) -> bool:
        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            return False

        self.repository.delete(restaurant)

        return True