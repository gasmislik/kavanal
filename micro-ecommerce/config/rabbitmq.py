from config.celery import app

def rabbitmq_producer():
    return app.producer_pool.acquire(block=True)


def publish(message, routing_key):
    with rabbitmq_producer() as producer:
        producer.publish(
            body=message,
            routing_key=routing_key,
            exchange='checkout'
        )