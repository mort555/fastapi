from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_by_restaurant(
        self,
        restaurant_id: int,
    ) -> list[Category]:
        return self.repository.get_all_by_restaurant(
            restaurant_id,
        )

    def get_by_id(
        self,
        category_id: int,
    ) -> Category | None:
        return self.repository.get_by_id(category_id)

    def create(
        self,
        restaurant_id: int,
        category_data: CategoryCreate,
    ) -> Category:
        category = Category(
            restaurant_id=restaurant_id,
            name=category_data.name,
        )

        return self.repository.create(category)

    def update(
        self,
        category_id: int,
        category_data: CategoryUpdate,
    ) -> Category | None:
        category = self.repository.get_by_id(category_id)

        if category is None:
            return None

        update_data = category_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(category, field, value)

        return self.repository.update(category)

    def delete(self, category_id: int) -> bool:
        category = self.repository.get_by_id(category_id)

        if category is None:
            return False

        self.repository.delete(category)

        return True