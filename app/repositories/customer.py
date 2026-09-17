from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Customer]:
        return (
            self.db.query(Customer)
            .order_by(Customer.id)
            .all()
        )

    def get_by_id(
        self,
        customer_id: int,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    def get_by_email(
        self,
        email: str,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )

    def create(
        self,
        customer: Customer,
    ) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def update(
        self,
        customer: Customer,
    ) -> Customer:
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def delete(
        self,
        customer: Customer,
    ) -> None:
        self.db.delete(customer)
        self.db.commit()