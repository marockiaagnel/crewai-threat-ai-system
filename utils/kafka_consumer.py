from kafka import KafkaConsumer, errors
import json
import time
from crew import ThreatAICrew
from dotenv import load_dotenv

load_dotenv()

def get_kafka_consumer():
    for attempt in range(10):  # Retry up to 10 times
        try:
            consumer = KafkaConsumer(
                "log-topic",
                bootstrap_servers="localhost:9092",
                auto_offset_reset="earliest",
                group_id="threat-detector",
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            print("✅ Connected to Kafka and subscribed to 'log-topic'")
            return consumer
        except errors.NoBrokersAvailable:
            print(f"⏳ Kafka broker not ready, retrying in 5s... ({attempt+1}/10)")
            time.sleep(5)
    raise RuntimeError("❌ Kafka broker not available after 10 retries")

consumer = get_kafka_consumer()

print("👂 Kafka consumer listening...")
try:
    for msg in consumer:
        try:
            log_data = msg.value.get("log", "")
            if not log_data:
                print("⚠️ Received message without 'log' key:", msg.value)
                continue
            print("\n🚀 Received log via Kafka:", log_data)
            crew = ThreatAICrew().get_crew(inputs={"logs": [log_data]})
            crew.kickoff()
        except Exception as e:
            print(f"❌ Error processing message: {e}")
except KeyboardInterrupt:
    print("\n🛑 Stopping consumer...")
finally:
    consumer.close()
    print("✅ Kafka consumer closed.")
