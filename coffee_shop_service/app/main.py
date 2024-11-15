from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from common.database import engine, Base as AppBase, get_db
from coffee_shop_service.app import coffee_shop_crud, schemas
from common.rabbitmq import consume_messages
import threading

app = FastAPI()

# AppBase.metadata.drop_all(bind=engine)
AppBase.metadata.create_all(bind=engine)


def start_rabbitmq_consumer():
    db = next(get_db())
    consume_messages(db)


threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()


@app.post("/coffees/{coffee_id}/add_to_shop/{coffee_shop_id}")
def add_coffee_to_shop(coffee_id: int, coffee_shop_id: int, db: Session = Depends(get_db)):
    coffee_shop_crud.add_coffee_to_shop(db, coffee_id, coffee_shop_id)
    return {"message": "Coffee added to coffee shop"}


@app.post("/coffees/{coffee_id}/remove_from_shop/{coffee_shop_id}")
def remove_coffee_from_shop(coffee_id: int, coffee_shop_id: int, db: Session = Depends(get_db)):
    coffee_shop_crud.remove_coffee_from_shop(db, coffee_id, coffee_shop_id)
    return {"message": "Coffee removed from coffee shop"}


@app.post("/coffee_shops", response_model=schemas.CoffeeShopResponse)
def add_coffee_shop(coffee_shop: schemas.CoffeeShopCreate, db: Session = Depends(get_db)):
    return coffee_shop_crud.create_coffee_shop(db, coffee_shop)


@app.get("/coffee_shops", response_model=list[schemas.CoffeeShopResponse])
def get_coffee_shops(db: Session = Depends(get_db)):
    return coffee_shop_crud.get_all_coffee_shops(db)