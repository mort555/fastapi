from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    dish_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    status: str


class CustomerMiniResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True,
    }


class RestaurantMiniResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True,
    }


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    dish_id: int
    name: str
    quantity: int
    price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True,
    }


class OrderStatusHistoryResponse(BaseModel):
    id: int
    order_id: int
    old_status: str | None
    new_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class OrderResponse(BaseModel):
    id: int
    customer: CustomerMiniResponse
    restaurant: RestaurantMiniResponse
    status: str
    items: list[OrderItemResponse] = Field(
        default_factory=list,
    )
    total_price: Decimal
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }