from dataclasses import dataclass

from app.core.filtering.base import BaseFilterParams


@dataclass
class RestaurantFilterParams(BaseFilterParams):
    is_active: bool | None = None
    min_rating: float | None = None