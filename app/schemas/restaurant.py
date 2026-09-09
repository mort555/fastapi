from datetime import datetime

from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None
    address: str
    phone: str


class RestaurantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: str | None
    address: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }