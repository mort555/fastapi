from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Category]:
        return (
            self.db.query(Category)
            .filter(Category.restaurant_id == restaurant_id)
            .all()
        )