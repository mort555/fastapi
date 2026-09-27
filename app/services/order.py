from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import (
    CustomerNotFoundError,
    DishNotAvailableError,
    DishNotFoundError,
    DishRestaurantMismatchError,
    InvalidOrderStatusError,
    OrderNotFoundError,
    RestaurantNotFoundError,
)
from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status_history import OrderStatusHistory
from app.repositories.order import OrderRepository
from app.schemas.order import OrderCreate


ALLOWED_TRANSITIONS = {
    "NEW": {"CONFIRMED", "CANCELLED"},
    "CONFIRMED": {"COOKING", "CANCELLED"},
    "COOKING": {"READY"},
    "READY": {"COMPLETED"},
    "COMPLETED": set(),
    "CANCELLED": set(),
}


class OrderService:
    def __init__(self, db: Session):
        self.repository = OrderRepository(db)

    def get_all(self) -> list[Order]:
        return self.repository.get_all()

    def get_by_id(
        self,
        order_id: int,
    ) -> Order | None:
        return self.repository.get_by_id(order_id)

    def _validate_customer(
        self,
        customer_id: int,
    ) -> None:
        customer = self.repository.get_customer(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundError()

    def _validate_restaurant(
        self,
        restaurant_id: int,
    ) -> None:
        restaurant = self.repository.get_restaurant(
            restaurant_id,
        )

        if restaurant is None:
            raise RestaurantNotFoundError()

    def _get_valid_dish(
        self,
        dish_id: int,
        restaurant_id: int,
    ) -> Dish:
        dish = self.repository.get_dish(dish_id)

        if dish is None:
            raise DishNotFoundError()

        if dish.restaurant_id != restaurant_id:
            raise DishRestaurantMismatchError()

        if not dish.is_available:
            raise DishNotAvailableError()

        return dish

    def _create_order(
        self,
        order_data: OrderCreate,
    ) -> Order:
        order = Order(
            customer_id=order_data.customer_id,
            restaurant_id=order_data.restaurant_id,
            status="NEW",
            total_price=Decimal("0"),
        )

        self.repository.create_order(order)

        return order

    def _add_order_item(
        self,
        order: Order,
        dish: Dish,
        quantity: int,
    ) -> Decimal:
        item_price = dish.price
        item_total = item_price * quantity

        order_item = OrderItem(
            order_id=order.id,
            dish_id=dish.id,
            quantity=quantity,
            price=item_price,
        )

        self.repository.create_order_item(
            order_item,
        )

        return item_total

    def _create_initial_history(
        self,
        order: Order,
    ) -> None:
        history = OrderStatusHistory(
            order_id=order.id,
            old_status=None,
            new_status="NEW",
        )

        self.repository.create_status_history(
            history,
        )

    def create(
        self,
        order_data: OrderCreate,
    ) -> Order:
        self._validate_customer(
            order_data.customer_id,
        )

        self._validate_restaurant(
            order_data.restaurant_id,
        )

        total_price = Decimal("0")

        try:
            order = self._create_order(
                order_data,
            )

            for item_data in order_data.items:
                dish = self._get_valid_dish(
                    item_data.dish_id,
                    order_data.restaurant_id,
                )

                total_price += self._add_order_item(
                    order,
                    dish,
                    item_data.quantity,
                )

            order.total_price = total_price

            self._create_initial_history(
                order,
            )

            self.repository.commit()
            self.repository.refresh(order)

            return order

        except Exception:
            self.repository.rollback()
            raise

    def change_status(
        self,
        order_id: int,
        new_status: str,
    ) -> Order:
        order = self.repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundError()

        new_status = new_status.upper()

        if new_status not in ALLOWED_TRANSITIONS.get(
            order.status,
            set(),
        ):
            raise InvalidOrderStatusError()

        old_status = order.status

        try:
            order.status = new_status

            history = OrderStatusHistory(
                order_id=order.id,
                old_status=old_status,
                new_status=new_status,
            )

            self.repository.create_status_history(
                history,
            )

            self.repository.commit()
            self.repository.refresh(order)

            return order

        except Exception:
            self.repository.rollback()
            raise