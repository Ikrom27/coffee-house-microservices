import pika
import json
from sqlalchemy.orm import Session

from coffee_shop_crud import toggle_coffee_shop_availability

RABBITMQ_HOST = "51.250.26.59"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest123"
QUEUE_NAME = "coffee_queue"

def process_message(ch, method, properties, body, db: Session):
    """
    Обработка сообщений из RabbitMQ для кофетериев.
    """
    try:
        data = json.loads(body)
        coffee_shop_id = data["coffee_shop_id"]
        action = data["action"]

        if action == "block":
            toggle_coffee_shop_availability(db, coffee_shop_id, False)  # Блокировка кофетерия
        elif action == "unblock":
            toggle_coffee_shop_availability(db, coffee_shop_id, True)  # Разблокировка кофетерия

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")

def consume_messages(db: Session):
    """
    Запуск консумера для обработки очереди RabbitMQ.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    print("RabbitMQ consumer запущен. Ожидание сообщений...")
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=lambda ch, method, properties, body: process_message(ch, method, properties, body, db),
    )
    channel.start_consuming()
