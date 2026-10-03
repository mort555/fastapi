from dataclasses import dataclass
from decimal import Decimal

from app.core.filtering.base import BaseFilterParams


@dataclass
class DishFilterParams(BaseFilterParams):
    category_id: int | None = None
    min_price: Decimal | None = None
    max_price: Decimal | None = None
    is_available: bool | None = None