import pika
import json
import time
import random

RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'tasks'


def produce():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    i = 0
    while True:
        data = {
            "task_id": i,
            "operation": random.choice(["add", "subtract", "multiply", "divide", "qwerty"]),
            "numbers": [random.randint(0, 10), random.randint(0, 10)]
        }
        i += 1
        message = json.dumps(data)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # Сообщение сохраняется при сбое
        )
        print(f"Отправлено: {message}")
        time.sleep(5)


if __name__ == '__main__':
    produce()
