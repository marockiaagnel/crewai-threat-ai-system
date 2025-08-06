from kafka import KafkaConsumer
import json
from crew import ThreatAICrew
from dotenv import load_dotenv

load_dotenv()

consumer = KafkaConsumer(
    "log-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="threat-detector",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("✅ Kafka consumer listening...")
for msg in consumer:
    log_data = msg.value["log"]
    print("\n🚀 Received log via Kafka:", log_data)
    crew = ThreatAICrew().get_crew(inputs={"logs": [log_data]})
    crew.kickoff()