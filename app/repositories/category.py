from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Category]:
        return (
            self.db.query(Category)
            .filter(Category.restaurant_id == restaurant_id)
            .all()
        )

    def get_by_id(
        self,
        category_id: int,
    ) -> Category | None:
        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)

        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()