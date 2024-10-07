from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
from typing import Dict, Any
from shared.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def get_kafka_consumer(group_id: str) -> KafkaConsumer:
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def produce_message(producer: KafkaProducer, message: Dict[str, Any]) -> None:
    try:
        future = producer.send(KAFKA_TOPIC, message)
        future.get(timeout=10)
        print(f"Message sent successfully: {message}")
    except KafkaError as e:
        print(f"Failed to send message: {e}")

def consume_messages(consumer: KafkaConsumer, callback):
    for message in consumer:
        callback(message.value)
