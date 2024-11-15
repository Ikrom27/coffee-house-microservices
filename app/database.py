from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:11111111@localhost:5432/coffee_house_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def show_current_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database();"))
        database_name = result.fetchone()[0]
        print(f"Подключено к базе данных: {database_name}")

# Выводим имя базы данных при старте
show_current_database()