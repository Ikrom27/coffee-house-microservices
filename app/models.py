from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Таблица связей многие ко многим между кофе и кофейнями
class CoffeeOfShop(Base):
    __tablename__ = 'coffee_of_shop'

    coffee_id = Column(Integer, ForeignKey('coffee.id'), primary_key=True)
    coffee_shop_id = Column(Integer, ForeignKey('coffee_shops.id'), primary_key=True)

# Модель кофейни
class CoffeeShop(Base):
    __tablename__ = 'coffee_shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    is_active = Column(Boolean, default=True)

    # Связь многие ко многим с кофе
    coffees = relationship('Coffee', secondary='coffee_of_shop', back_populates="coffee_shops")

    def __repr__(self):
        return f"<CoffeeShop(name={self.name}, location={self.location})>"

# Модель кофе
class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)

    # Связь многие ко многим с кофейнями
    coffee_shops = relationship('CoffeeShop', secondary='coffee_of_shop', back_populates="coffees")

    def __repr__(self):
        return f"<Coffee(name={self.name}, price={self.price}, available={self.is_available})>"
