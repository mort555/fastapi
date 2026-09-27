from typing import Generic, TypeVar

from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        object_id: int,
    ) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == object_id).first()

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).order_by(self.model.id).all()

    def create(
        self,
        obj: ModelType,
    ) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def update(
        self,
        obj: ModelType,
    ) -> ModelType:
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(
        self,
        obj: ModelType,
    ) -> None:
        self.db.delete(obj)
        self.db.commit()
