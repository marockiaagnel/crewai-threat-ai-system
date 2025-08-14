import os
import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "threat-logs")

# Wait until Kafka is available
for i in range(60):  # 60 seconds max wait
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ Kafka is ready!")
        break
    except NoBrokersAvailable:
        print(f"⏳ Waiting for Kafka... ({i+1}/60)")
        time.sleep(1)
else:
    raise RuntimeError("Kafka not available after 60 seconds")

def send_log_to_kafka(log):
    try:
        producer.send(KAFKA_TOPIC, log)
        producer.flush()
        print(f"✅ Log sent to Kafka topic '{KAFKA_TOPIC}'")
    except Exception as e:
        print(f"❌ Failed to send log to Kafka: {e}")
