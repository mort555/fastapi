

from sqlalchemy.orm import Session, joinedload

from app.core.filtering import FilterMixin, OrderFilterParams
from app.models.customer import Customer
from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status_history import OrderStatusHistory
from app.models.restaurant import Restaurant
from app.repositories.base import BaseRepository


class OrderRepository(
    BaseRepository[Order],
    FilterMixin,
):
    model = Order

    def __init__(self, db: Session):
        super().__init__(db)

    def _get_order_query(self):
        return self.db.query(Order).options(
            joinedload(Order.customer),
            joinedload(Order.restaurant),
            joinedload(Order.items).joinedload(
                OrderItem.dish,
            ),
        )

    def get_all(self) -> list[Order]:
        return (
            self._get_order_query()
            .order_by(Order.id)
            .all()
        )

    def get_by_id(
        self,
        order_id: int,
    ) -> Order | None:
        return (
            self._get_order_query()
            .filter(Order.id == order_id)
            .first()
        )

    def get_filtered(
        self,
        params: OrderFilterParams,
    ) -> tuple[list[Order], int]:
        query = self._get_order_query()

        if params.status:
            query = query.filter(
                Order.status == params.status.upper(),
            )

        if params.customer_id is not None:
            query = query.filter(
                Order.customer_id == params.customer_id,
            )

        if params.restaurant_id is not None:
            query = query.filter(
                Order.restaurant_id == params.restaurant_id,
            )

        if params.date_from is not None:
            query = query.filter(
                Order.created_at >= params.date_from,
            )

        if params.date_to is not None:
            query = query.filter(
                Order.created_at <= params.date_to,
            )

        allowed_fields = {
            "id": Order.id,
            "created_at": Order.created_at,
            "total_price": Order.total_price,
            "status": Order.status,
        }

        query = self.apply_ordering(
            query,
            params.ordering,
            allowed_fields,
            Order.id,
        )

        total = query.order_by(None).count()

        items = (
            query
            .offset(params.offset)
            .limit(params.page_size)
            .all()
        )

        return items, total

    def get_customer(
        self,
        customer_id: int,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    def get_restaurant(
        self,
        restaurant_id: int,
    ) -> Restaurant | None:
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )

    def get_dish(
        self,
        dish_id: int,
    ) -> Dish | None:
        return (
            self.db.query(Dish)
            .filter(Dish.id == dish_id)
            .first()
        )

    def create_order(
        self,
        order: Order,
    ) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def create_order_item(
        self,
        order_item: OrderItem,
    ) -> OrderItem:
        self.db.add(order_item)
        self.db.flush()
        return order_item

    def create_status_history(
        self,
        history: OrderStatusHistory,
    ) -> OrderStatusHistory:
        self.db.add(history)
        self.db.flush()
        return history

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        order: Order,
    ) -> None:
        self.db.refresh(order)