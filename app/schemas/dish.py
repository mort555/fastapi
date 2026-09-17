from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class DishCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    weight: int
    category_id: int


class DishUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    weight: int | None = None
    category_id: int | None = None
    is_available: bool | None = None


class DishResponse(BaseModel):
    id: int
    restaurant_id: int
    category_id: int
    name: str
    description: str | None
    price: Decimal
    weight: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class DishListResponse(BaseModel):
    items: list[DishResponse]
    page: int
    page_size: int
    total: int
    pages: int