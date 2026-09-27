from datetime import datetime, timedelta
from decimal import Decimal

from app.core.database import SessionLocal
from app.models.category import Category
from app.models.customer import Customer
from app.models.dish import Dish
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status_history import OrderStatusHistory
from app.models.restaurant import Restaurant
from app.models.review import Review


def seed_restaurants(db):
    restaurants = [
        Restaurant(
            name="Burger House",
            description="Бургеры и американская кухня",
            address="вул. Хрещатик, 10",
            phone="+380671111111",
            is_active=True,
        ),
        Restaurant(
            name="Pizza Place",
            description="Пицца и итальянская кухня",
            address="вул. Лесі Українки, 25",
            phone="+380672222222",
            is_active=True,
        ),
    ]

    db.add_all(restaurants)
    db.flush()

    return restaurants


def seed_categories(db, restaurants):
    categories = [
        Category(
            restaurant_id=restaurants[0].id,
            name="Бургеры",
            description="Фирменные бургеры",
        ),
        Category(
            restaurant_id=restaurants[0].id,
            name="Картофель",
            description="Картофель и снеки",
        ),
        Category(
            restaurant_id=restaurants[0].id,
            name="Напитки",
            description="Холодные напитки",
        ),
        Category(
            restaurant_id=restaurants[1].id,
            name="Пицца",
            description="Пицца на тонком тесте",
        ),
        Category(
            restaurant_id=restaurants[1].id,
            name="Паста",
            description="Итальянская паста",
        ),
        Category(
            restaurant_id=restaurants[1].id,
            name="Напитки",
            description="Напитки",
        ),
    ]

    db.add_all(categories)
    db.flush()

    return categories


def seed_dishes(db, categories, restaurants):
    dishes = [
        Dish(
            restaurant_id=restaurants[0].id,
            category_id=categories[0].id,
            name="Classic Burger",
            description="Классический бургер с говядиной",
            price=Decimal("220.00"),
            weight=300,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[0].id,
            category_id=categories[0].id,
            name="Cheese Burger",
            description="Бургер с сыром",
            price=Decimal("250.00"),
            weight=320,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[0].id,
            category_id=categories[1].id,
            name="French Fries",
            description="Картофель фри",
            price=Decimal("90.00"),
            weight=150,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[0].id,
            category_id=categories[2].id,
            name="Cola",
            description="Холодная Coca-Cola",
            price=Decimal("60.00"),
            weight=500,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[1].id,
            category_id=categories[3].id,
            name="Margherita",
            description="Пицца с томатами и моцареллой",
            price=Decimal("280.00"),
            weight=500,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[1].id,
            category_id=categories[3].id,
            name="Pepperoni",
            description="Пицца с пепперони",
            price=Decimal("330.00"),
            weight=550,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[1].id,
            category_id=categories[4].id,
            name="Carbonara",
            description="Паста карбонара",
            price=Decimal("260.00"),
            weight=350,
            is_available=True,
        ),
        Dish(
            restaurant_id=restaurants[1].id,
            category_id=categories[5].id,
            name="Lemonade",
            description="Домашний лимонад",
            price=Decimal("100.00"),
            weight=500,
            is_available=True,
        ),
    ]

    db.add_all(dishes)
    db.flush()

    return dishes


def seed_customers(db):
    customers = [
        Customer(
            name="Иван Петров",
            email="seed.ivan@example.com",
            phone="+380631111111",
        ),
        Customer(
            name="Анна Коваленко",
            email="seed.anna@example.com",
            phone="+380632222222",
        ),
        Customer(
            name="Максим Бондарь",
            email="seed.maksym@example.com",
            phone="+380633333333",
        ),
        Customer(
            name="Олена Шевченко",
            email="seed.olena@example.com",
            phone="+380634444444",
        ),
        Customer(
            name="Дмитрий Мельник",
            email="seed.dmytro@example.com",
            phone="+380635555555",
        ),
    ]

    db.add_all(customers)
    db.flush()

    return customers


def seed_orders(db, restaurants, dishes, customers):
    now = datetime.utcnow()

    order_1 = Order(
        customer_id=customers[0].id,
        restaurant_id=restaurants[0].id,
        status="COMPLETED",
        total_price=Decimal("830.00"),
        created_at=now - timedelta(days=5),
        updated_at=now - timedelta(days=5),
    )

    order_2 = Order(
        customer_id=customers[1].id,
        restaurant_id=restaurants[0].id,
        status="COMPLETED",
        total_price=Decimal("340.00"),
        created_at=now - timedelta(days=3),
        updated_at=now - timedelta(days=3),
    )

    order_3 = Order(
        customer_id=customers[2].id,
        restaurant_id=restaurants[1].id,
        status="COMPLETED",
        total_price=Decimal("790.00"),
        created_at=now - timedelta(days=2),
        updated_at=now - timedelta(days=2),
    )

    order_4 = Order(
        customer_id=customers[3].id,
        restaurant_id=restaurants[1].id,
        status="CANCELLED",
        total_price=Decimal("330.00"),
        created_at=now - timedelta(days=1),
        updated_at=now - timedelta(days=1),
    )

    order_5 = Order(
        customer_id=customers[4].id,
        restaurant_id=restaurants[0].id,
        status="NEW",
        total_price=Decimal("250.00"),
        created_at=now,
        updated_at=now,
    )

    orders = [
        order_1,
        order_2,
        order_3,
        order_4,
        order_5,
    ]

    db.add_all(orders)
    db.flush()

    return orders


def seed_order_items(db, orders, dishes):
    order_items = [
        OrderItem(
            order_id=orders[0].id,
            dish_id=dishes[0].id,
            quantity=2,
            price=dishes[0].price,
        ),
        OrderItem(
            order_id=orders[0].id,
            dish_id=dishes[2].id,
            quantity=1,
            price=dishes[2].price,
        ),
        OrderItem(
            order_id=orders[0].id,
            dish_id=dishes[3].id,
            quantity=5,
            price=dishes[3].price,
        ),
        OrderItem(
            order_id=orders[1].id,
            dish_id=dishes[1].id,
            quantity=1,
            price=dishes[1].price,
        ),
        OrderItem(
            order_id=orders[1].id,
            dish_id=dishes[2].id,
            quantity=1,
            price=dishes[2].price,
        ),
        OrderItem(
            order_id=orders[3].id,
            dish_id=dishes[5].id,
            quantity=1,
            price=dishes[5].price,
        ),
        OrderItem(
            order_id=orders[4].id,
            dish_id=dishes[1].id,
            quantity=1,
            price=dishes[1].price,
        ),
        OrderItem(
            order_id=orders[2].id,
            dish_id=dishes[5].id,
            quantity=1,
            price=dishes[5].price,
        ),
        OrderItem(
            order_id=orders[2].id,
            dish_id=dishes[6].id,
            quantity=1,
            price=dishes[6].price,
        ),
        OrderItem(
            order_id=orders[2].id,
            dish_id=dishes[7].id,
            quantity=2,
            price=dishes[7].price,
        ),
    ]

    db.add_all(order_items)
    db.flush()

    return order_items


def seed_order_status_history(db, orders):
    history = [
        OrderStatusHistory(
            order_id=orders[0].id,
            old_status=None,
            new_status="NEW",
        ),
        OrderStatusHistory(
            order_id=orders[0].id,
            old_status="NEW",
            new_status="CONFIRMED",
        ),
        OrderStatusHistory(
            order_id=orders[0].id,
            old_status="CONFIRMED",
            new_status="COOKING",
        ),
        OrderStatusHistory(
            order_id=orders[0].id,
            old_status="COOKING",
            new_status="READY",
        ),
        OrderStatusHistory(
            order_id=orders[0].id,
            old_status="READY",
            new_status="COMPLETED",
        ),
        OrderStatusHistory(
            order_id=orders[1].id,
            old_status=None,
            new_status="NEW",
        ),
        OrderStatusHistory(
            order_id=orders[1].id,
            old_status="NEW",
            new_status="CONFIRMED",
        ),
        OrderStatusHistory(
            order_id=orders[1].id,
            old_status="CONFIRMED",
            new_status="COOKING",
        ),
        OrderStatusHistory(
            order_id=orders[1].id,
            old_status="COOKING",
            new_status="READY",
        ),
        OrderStatusHistory(
            order_id=orders[1].id,
            old_status="READY",
            new_status="COMPLETED",
        ),
        OrderStatusHistory(
            order_id=orders[2].id,
            old_status=None,
            new_status="NEW",
        ),
        OrderStatusHistory(
            order_id=orders[2].id,
            old_status="NEW",
            new_status="CONFIRMED",
        ),
        OrderStatusHistory(
            order_id=orders[2].id,
            old_status="CONFIRMED",
            new_status="COOKING",
        ),
        OrderStatusHistory(
            order_id=orders[2].id,
            old_status="COOKING",
            new_status="READY",
        ),
        OrderStatusHistory(
            order_id=orders[2].id,
            old_status="READY",
            new_status="COMPLETED",
        ),
        OrderStatusHistory(
            order_id=orders[3].id,
            old_status=None,
            new_status="NEW",
        ),
        OrderStatusHistory(
            order_id=orders[3].id,
            old_status="NEW",
            new_status="CANCELLED",
        ),
        OrderStatusHistory(
            order_id=orders[4].id,
            old_status=None,
            new_status="NEW",
        ),
    ]

    db.add_all(history)
    db.flush()

    return history


def seed_reviews(db, restaurants, customers):
    reviews = [
        Review(
            customer_id=customers[0].id,
            restaurant_id=restaurants[0].id,
            rating=5,
            text="Очень вкусные бургеры!",
        ),
        Review(
            customer_id=customers[1].id,
            restaurant_id=restaurants[0].id,
            rating=4,
            text="Хорошее место.",
        ),
        Review(
            customer_id=customers[2].id,
            restaurant_id=restaurants[1].id,
            rating=5,
            text="Отличная пицца!",
        ),
    ]

    db.add_all(reviews)
    db.flush()

    return reviews


def run_all():
    db = SessionLocal()

    try:
        restaurants = seed_restaurants(db)

        categories = seed_categories(
            db,
            restaurants,
        )

        dishes = seed_dishes(
            db,
            categories,
            restaurants,
        )

        customers = seed_customers(db)

        orders = seed_orders(
            db,
            restaurants,
            dishes,
            customers,
        )

        seed_order_items(
            db,
            orders,
            dishes,
        )

        seed_order_status_history(
            db,
            orders,
        )

        seed_reviews(
            db,
            restaurants,
            customers,
        )

        db.commit()

        print("Seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_all()