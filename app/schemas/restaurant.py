from datetime import datetime
from decimal import Decimal

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
    rating: Decimal
    reviews_count: int

    model_config = {
        "from_attributes": True,
    }


class RestaurantListResponse(BaseModel):
    items: list[RestaurantResponse]
    page: int
    page_size: int
    total: int
    pages: int


class RestaurantStatisticsResponse(BaseModel):
    orders_count: int
    total_sales: Decimal
    average_order_price: Decimal
    top_dishes: list["TopDishResponse"]


class TopDishResponse(BaseModel):
    dish_id: int
    dish_name: str
    quantity: int
    sales: Decimal


class RestaurantSalesResponse(BaseModel):
    date_from: datetime
    date_to: datetime
    orders_count: int
    total_sales: Decimal