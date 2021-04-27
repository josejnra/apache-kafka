import json
import random

from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})
size = 1000000


def get_message(size: int) -> bytes:
    for _ in range(size):
        yield json.dumps({
            "nome": random.choice(["john", "alex", "jack", "whindersson"]),
            "id": random.randint(1, 1000)
        }).encode()


def delivery_report(err, decoded_message, original_message):
    if err is not None:
        print(err)


def confluent_producer_async():
    for msg in get_message(size):
        producer.produce(
            "topic1",
            msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
    producer.flush()


def confluent_producer_sync():
    for msg in get_message(size):
        producer.produce(
            "topic1",
            msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
        producer.flush()


if __name__ == '__main__':
    confluent_producer_async()
