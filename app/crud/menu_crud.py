from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Coffee, CoffeeOfShop, CoffeeShop
from app.schemas import CoffeeCreate

def create_coffee(db: Session, coffee: CoffeeCreate) -> Coffee:
    db_coffee = Coffee(name=coffee.name, description=coffee.description, price=coffee.price)
    db.add(db_coffee)
    db.commit()
    db.refresh(db_coffee)
    return db_coffee

def get_all_coffees(db: Session) -> list[Coffee]:
    return db.query(Coffee).all()


def add_coffee_to_shop(db: Session, coffee_id: int, coffee_shop_id: int):
    coffee_shop = db.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()

    if coffee_shop is None:
        raise ValueError(f"Coffee shop with ID {coffee_shop_id} does not exist.")
    coffee_of_shop = CoffeeOfShop(coffee_id=coffee_id, coffee_shop_id=coffee_shop_id)

    try:
        db.add(coffee_of_shop)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Failed to add coffee to shop: {str(e)}")

def remove_coffee_from_shop(db: Session, coffee_id: int, coffee_shop_id: int):
    coffee_of_shop = db.query(CoffeeOfShop).filter(
        CoffeeOfShop.coffee_id == coffee_id,
        CoffeeOfShop.coffee_shop_id == coffee_shop_id
    ).first()
    if coffee_of_shop:
        db.delete(coffee_of_shop)
        db.commit()

def toggle_coffee_availability(db: Session, coffee_id: int, available: bool):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if coffee:
        coffee.is_available = available
        db.commit()
        db.refresh(coffee)
    return coffee


def get_coffees_by_shop(db: Session, coffee_shop_id: int):
    coffees = db.query(Coffee).join(CoffeeOfShop).filter(CoffeeOfShop.coffee_shop_id == coffee_shop_id).all()
    return [
        {
            "id": coffee.id,
            "name": coffee.name,
            "description": coffee.description,
            "price": coffee.price,
            "is_available": coffee.is_available,
            "coffee_shops": [coffee_shop.id for coffee_shop in coffee.coffee_shops]
        }
        for coffee in coffees
    ]
