from sqlalchemy.orm import Session
from app.models import CoffeeShop, CoffeeOfShop
from app.schemas import CoffeeShopCreate

# Функция для добавления новой кофейни
def create_coffee_shop(db: Session, coffee_shop: CoffeeShopCreate) -> CoffeeShop:
    db_coffee_shop = CoffeeShop(name=coffee_shop.name, location=coffee_shop.location)
    db.add(db_coffee_shop)
    db.commit()
    db.refresh(db_coffee_shop)
    return db_coffee_shop

# Функция для получения всех кофеен
def get_all_coffee_shops(db: Session) -> list[CoffeeShop]:
    return db.query(CoffeeShop).all()

# Функция для получения всех кофе в кофейне
def get_coffees_by_shop(db: Session, coffee_shop_id: int) -> list[CoffeeShop]:
    return db.query(CoffeeShop).join(CoffeeOfShop).filter(CoffeeOfShop.coffee_shop_id == coffee_shop_id).all()
