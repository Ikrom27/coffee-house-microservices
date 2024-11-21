import threading

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from common.database import engine, Base as AppBase, get_db
from common.models import Coffee
from common.models import *
from rabbitmq import consume_messages
import schemas
import menu_crud

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


@app.post("/coffees/{coffee_id}/block")
def block_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = menu_crud.toggle_coffee_availability(db, coffee_id, False)
    if coffee:
        return {"message": "Кофе успешно заблокирован", "coffee": coffee}
    return {"error": "Кофе не найден"}


@app.post("/coffees/{coffee_id}/unblock")
def unblock_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = menu_crud.toggle_coffee_availability(db, coffee_id, True)
    if coffee:
        return {"message": "Кофе успешно разблокирован", "coffee": coffee}
    return {"error": "Кофе не найден"}


@app.delete("/coffees/{coffee_id}")
def delete_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if coffee:
        db.delete(coffee)
        db.commit()
        return {"message": "Кофе успешно удален"}
    return {"error": "Кофе не найден"}


@app.get("/coffees", response_model=list[schemas.CoffeeResponse])
def get_coffees(db: Session = Depends(get_db)):
    return menu_crud.get_all_coffees(db)


@app.get("/coffee_shops/{coffee_shop_id}/coffees", response_model=list[schemas.CoffeeResponse])
def get_coffees_by_shop(coffee_shop_id: int, db: Session = Depends(get_db)):
    return menu_crud.get_coffees_by_shop(db, coffee_shop_id)
