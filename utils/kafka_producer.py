from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_log = {
    "log": "\n".join([
        "Received: from mail.example.com (203.0.113.45) by secure.domain.com",
        "Subject: Reset Password",
        "To: user@example.com",
        "Content: http://malicious.com/reset"
    ])
}

producer.send("log-topic", sample_log)
producer.flush()
print("Log sent to Kafka.")