from sqlalchemy.orm import Session

from common.models import CoffeeShop, CoffeeOfShop, Coffee
from menu_service.app.schemas import CoffeeCreate, CoffeeResponse


def create_coffee(db: Session, coffee: CoffeeCreate) -> Coffee:
    db_coffee = Coffee(name=coffee.name, description=coffee.description, price=coffee.price)
    db.add(db_coffee)
    db.commit()
    db.refresh(db_coffee)
    return db_coffee


def get_all_coffees(db: Session) -> list[Coffee]:
    return db.query(Coffee).all()


def toggle_coffee_availability(db: Session, coffee_id: int, available: bool):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if coffee:
        coffee.is_available = available
        db.commit()
        db.refresh(coffee)
    return coffee


def get_coffees_by_shop(db: Session, coffee_shop_id: int) -> list[dict]:
    coffees = (
        db.query(Coffee)
        .join(CoffeeOfShop)
        .filter(CoffeeOfShop.coffee_shop_id == coffee_shop_id)
        .all()
    )
    result = []
    for coffee in coffees:
        coffee_shops_ids = [
            shop.id for shop in coffee.coffee_shops
        ]
        result.append({
            "id": coffee.id,
            "name": coffee.name,
            "description": coffee.description,
            "price": coffee.price,
            "is_available": coffee.is_available,
            "coffee_shops": coffee_shops_ids,
        })
    return result

