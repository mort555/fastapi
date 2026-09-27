from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_serializer


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
    rating: Decimal
    reviews_count: int

    model_config = {
        "from_attributes": True,
    }

    @field_serializer("rating")
    def serialize_rating(self, value: Decimal) -> str:
        return f"{value:.2f}"


class RestaurantListResponse(BaseModel):
    items: list[RestaurantResponse]
    page: int
    page_size: int
    total: int
    pages: int


class TopDishResponse(BaseModel):
    dish_id: int
    name: str
    quantity: int
    revenue: Decimal


class RestaurantStatisticsResponse(BaseModel):
    orders_count: int
    completed_orders: int
    cancelled_orders: int
    revenue: Decimal
    average_order_price: Decimal
    average_rating: Decimal

    @field_serializer(
        "revenue",
        "average_order_price",
        "average_rating",
    )
    def serialize_decimal(self, value: Decimal) -> str:
        return f"{value:.2f}"


class RestaurantSalesResponse(BaseModel):
    date_from: datetime
    date_to: datetime
    orders: int
    revenue: Decimal
    top_dishes: list[TopDishResponse]

    @field_serializer("revenue")
    def serialize_revenue(self, value: Decimal) -> str:
        return f"{value:.2f}"