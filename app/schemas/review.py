from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    rating: int = Field(
        ge=1,
        le=5,
    )
    text: str | None = None


class ReviewResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    rating: int
    text: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }