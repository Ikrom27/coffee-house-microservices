from pydantic import BaseModel
from typing import List


class CoffeeShopCreate(BaseModel):
    name: str
    location: str


class CoffeeShopResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool

    class Config:
        orm_mode = True
