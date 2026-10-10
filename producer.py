import time
import random
import json
from kafka import KafkaProducer

# Connect to our Docker Kafka (using port 29092 as defined in docker-compose)
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Dummy data to simulate a live stream of brand feedback

sample_texts = [
    "I absolutely love the new iPhone, the camera is amazing!",
    "Terrible customer service, I waited on hold for 2 hours.",
    "The battery life is okay, nothing special but it works.",
    "Best purchase I have made this year. Highly recommend!",
    "My screen broke after one day. Total garbage.",
    "Delivery was late, but the product is fine.",
    "Wow, this update completely ruined the app. So slow now.",
    "The UI is so clean and easy to use.",
    "I'm extremely disappointed with the latest patch.",
    "Five stars! Will definitely buy again."
]

print("Starting to stream data to Kafka... (Press Ctrl+C to stop)")
try:
    while True:
        data = {
            "text": random.choice(sample_texts),
            "timestamp": int(time.time() * 1000) # Milliseconds for Elasticsearch
        }
        producer.send('live_reviews', value=data)
        print(f"Sent: {data['text']}")
        time.sleep(random.uniform(0.5, 2.0)) # Send a message every 0.5 to 2 seconds
except KeyboardInterrupt:
    print("\nStreaming stopped.")
