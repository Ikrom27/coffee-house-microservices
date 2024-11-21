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

    class Config:
        orm_mode = True