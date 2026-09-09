from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Restaurant]:
        return self.db.query(Restaurant).all()

    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )

    def create(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    def update(self, restaurant: Restaurant) -> Restaurant:
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    def delete(self, restaurant: Restaurant) -> None:
        self.db.delete(restaurant)
        self.db.commit()