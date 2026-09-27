from dataclasses import dataclass
from math import ceil


@dataclass
class FilterParams:
    page: int = 1
    page_size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    def get_pages(self, total: int) -> int:
        if total == 0:
            return 0

        return ceil(total / self.page_size)