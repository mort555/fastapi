from decimal import Decimal

from sqlalchemy.orm import Session

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

    def create(
        self,
        order_data: OrderCreate,
    ) -> Order:
        customer = self.repository.get_customer(
            order_data.customer_id,
        )

        if customer is None:
            raise ValueError("Customer not found")

        restaurant = self.repository.get_restaurant(
            order_data.restaurant_id,
        )

        if restaurant is None:
            raise ValueError("Restaurant not found")

        total_price = Decimal("0")

        order = Order(
            customer_id=order_data.customer_id,
            restaurant_id=order_data.restaurant_id,
            status="NEW",
            total_price=Decimal("0"),
        )

        try:
            self.repository.create_order(order)

            for item_data in order_data.items:
                dish = self.repository.get_dish(
                    item_data.dish_id,
                )

                if dish is None:
                    raise ValueError(
                        f"Dish {item_data.dish_id} not found",
                    )

                if dish.restaurant_id != order_data.restaurant_id:
                    raise ValueError(
                        f"Dish {item_data.dish_id} "
                        "does not belong to this restaurant",
                    )

                if not dish.is_available:
                    raise ValueError(
                        f"Dish {item_data.dish_id} is not available",
                    )

                item_price = dish.price
                item_total = item_price * item_data.quantity

                total_price += item_total

                order_item = OrderItem(
                    order_id=order.id,
                    dish_id=dish.id,
                    quantity=item_data.quantity,
                    price=item_price,
                )

                self.repository.create_order_item(
                    order_item,
                )

            order.total_price = total_price

            history = OrderStatusHistory(
                order_id=order.id,
                old_status=None,
                new_status="NEW",
            )

            self.repository.create_status_history(history)

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
            raise ValueError("Order not found")

        new_status = new_status.upper()

        if new_status not in ALLOWED_TRANSITIONS.get(
            order.status,
            set(),
        ):
            raise ValueError(
                f"Invalid status transition: "
                f"{order.status} -> {new_status}",
            )

        old_status = order.status

        try:
            order.status = new_status

            history = OrderStatusHistory(
                order_id=order.id,
                old_status=old_status,
                new_status=new_status,
            )

            self.repository.create_status_history(history)

            self.repository.commit()
            self.repository.refresh(order)

            return order

        except Exception:
            self.repository.rollback()
            raise