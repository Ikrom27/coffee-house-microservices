from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from coffee_shop_service.app.schemas import CoffeeShopCreate
from common.models import CoffeeShop, CoffeeOfShop


def create_coffee_shop(db: Session, coffee_shop: CoffeeShopCreate) -> CoffeeShop:
    db_coffee_shop = CoffeeShop(name=coffee_shop.name, location=coffee_shop.location)
    db.add(db_coffee_shop)
    db.commit()
    db.refresh(db_coffee_shop)
    return db_coffee_shop


def get_all_coffee_shops(db: Session) -> list[CoffeeShop]:
    return db.query(CoffeeShop).all()


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


# uvicorn coffee_shop_service.app.main:app --reload --host 0.0.0.0 --port 8000
# uvicorn menu_service.app.main:app --reload --host 0.0.0.0 --port 8001