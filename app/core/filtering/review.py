from dataclasses import dataclass

from app.core.filtering.base import BaseFilterParams


@dataclass
class ReviewFilterParams(BaseFilterParams):
    restaurant_id: int | None = None
    customer_id: int | None = None
    min_rating: int | None = None
    max_rating: int | None = None