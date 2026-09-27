from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status_history import OrderStatusHistory
from app.models.restaurant import Restaurant
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model = Order

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self) -> list[Order]:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.restaurant),
                joinedload(Order.items).joinedload(
                    OrderItem.dish,
                ),
            )
            .order_by(Order.id)
            .all()
        )

    def get_by_id(
        self,
        order_id: int,
    ) -> Order | None:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.restaurant),
                joinedload(Order.items).joinedload(
                    OrderItem.dish,
                ),
            )
            .filter(Order.id == order_id)
            .first()
        )

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