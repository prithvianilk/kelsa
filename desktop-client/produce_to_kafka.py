import json
from kafka import KafkaProducer
import time

bootstrap_servers = 'localhost:9092'
topic_name = 'work-topic'

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=1000
)

message_data = {
    "application": "vscode",
    "tab": "kelsa",
    "timestamp": int(time.time() * 1000)
}

for i in range(1, 1001):
    try:
        # Update timestamp for each message to be unique
        message_data['timestamp'] = int(time.time() * 1000)
        producer.send(topic_name, value=message_data)
        print(f"Sent iteration {i} to topic '{topic_name}'")
    except Exception as e:
        print(f"Error sending message on iteration {i}: {e}")
        break
    time.sleep(0.1)

producer.flush()

print("\nAll iterations complete.")