from dataclasses import dataclass
from math import ceil
from typing import Any

from sqlalchemy.orm import Query


@dataclass
class BaseFilterParams:
    search: str | None = None
    ordering: str | None = None
    page: int = 1
    page_size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    def get_pages(self, total: int) -> int:
        if total == 0:
            return 0

        return ceil(total / self.page_size)


class FilterMixin:
    def apply_search(
        self,
        query: Query,
        field: Any,
        search: str | None,
    ) -> Query:
        if search:
            query = query.filter(
                field.ilike(f"%{search}%"),
            )

        return query

    def apply_is_active(
        self,
        query: Query,
        field: Any,
        is_active: bool | None,
    ) -> Query:
        if is_active is not None:
            query = query.filter(
                field == is_active,
            )

        return query

    def apply_ordering(
        self,
        query: Query,
        ordering: str | None,
        allowed_fields: dict[str, Any],
        default_field: Any,
    ) -> Query:
        if ordering:
            descending = ordering.startswith("-")
            field_name = ordering.lstrip("-")

            field = allowed_fields.get(field_name)

            if field is not None:
                if descending:
                    query = query.order_by(field.desc())
                else:
                    query = query.order_by(field.asc())

                return query

        return query.order_by(default_field)

    def paginate(
        self,
        query: Query,
        params: BaseFilterParams,
    ) -> tuple[list[Any], int]:
        total = query.count()

        items = (
            query
            .offset(params.offset)
            .limit(params.page_size)
            .all()
        )

        return items, total