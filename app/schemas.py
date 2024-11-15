from pydantic import BaseModel
from typing import List

class CoffeeCreate(BaseModel):
    name: str
    description: str
    price: int

class CoffeeResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_available: bool
    coffee_shops: List[int]

    class Config:
        orm_mode = True

class CoffeeShopCreate(BaseModel):
    name: str
    location: str

class CoffeeShopResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool
    coffees: List[int]

    class Config:
        orm_mode = True
