from dataclasses import dataclass
from datetime import datetime

from app.core.filtering.base import BaseFilterParams


@dataclass
class OrderFilterParams(BaseFilterParams):
    status: str | None = None
    customer_id: int | None = None
    restaurant_id: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None