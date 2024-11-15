import threading

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from common.database import engine, Base as AppBase, get_db
from common.rabbitmq import consume_messages
from menu_service.app import schemas
from menu_service.app import menu_crud

app = FastAPI()

# AppBase.metadata.drop_all(bind=engine)
AppBase.metadata.create_all(bind=engine)


def start_rabbitmq_consumer():
    db = next(get_db())
    consume_messages(db)


threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()


@app.post("/coffees", response_model=schemas.CoffeeResponse)
def add_coffee(coffee: schemas.CoffeeCreate, db: Session = Depends(get_db)):
    return menu_crud.create_coffee(db, coffee)


@app.get("/coffees", response_model=list[schemas.CoffeeResponse])
def get_coffees(db: Session = Depends(get_db)):
    return menu_crud.get_all_coffees(db)


@app.get("/coffee_shops/{coffee_shop_id}/coffees", response_model=list[schemas.CoffeeResponse])
def get_coffees_by_shop(coffee_shop_id: int, db: Session = Depends(get_db)):
    return menu_crud.get_coffees_by_shop(db, coffee_shop_id)