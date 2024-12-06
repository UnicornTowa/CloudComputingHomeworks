import pika
import json
import logging

RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'tasks'
DLQ_NAME = 'tasks_dlq'

logging.basicConfig(level=logging.INFO)


def process_message(ch, method, properties, body):
    try:
        task = json.loads(body)
        logging.info(f"Обработка задачи: {task}")

        operation = task["operation"]
        num1, num2 = task["numbers"]

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                raise ValueError("Деление на ноль")
            result = num1 / num2
        else:
            raise ValueError(f"Неизвестная операция: {operation}")

        logging.info(f"Результат задачи: {result}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Ошибка задачи: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        dlq_channel.basic_publish(exchange='', routing_key=DLQ_NAME, body=body)


# Настройка соединения RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
dlq_channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)
dlq_channel.queue_declare(queue=DLQ_NAME, durable=True)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

if __name__ == '__main__':
    logging.info("Потребитель запущен")
    channel.start_consuming()
