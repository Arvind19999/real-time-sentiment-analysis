import json
from kafka import KafkaConsumer
from textblob import TextBlob
from elasticsearch import Elasticsearch

# Connect to Kafka and Elasticsearch (using port 29092 as defined in docker-compose)
consumer = KafkaConsumer(
    'live_reviews',
    bootstrap_servers=['localhost:29092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)
es = Elasticsearch("http://localhost:9200")

print("Listening for messages on 'live_reviews' topic and processing sentiment...")

for message in consumer:
    record = message.value
    text = record['text']
    
    # Calculate sentiment using TextBlob
    analysis = TextBlob(text)
    polarity_score = analysis.sentiment.polarity
    
    # Label it
    if polarity_score > 0.1:
        sentiment_label = "Positive"
    elif polarity_score < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    # Create the final document
    doc = {
        "text": text,
        "sentiment_score": polarity_score,
        "sentiment_label": sentiment_label,
        "timestamp": record['timestamp']
    }
    
    # Send to Elasticsearch (using body for es client < 8.0 compat)
    try:
        es.index(index="sentiment_data", document=doc)
        print(f"Processed & Stored: [{sentiment_label}] {text}")
    except Exception as e:
        print(f"Failed to store in Elasticsearch: {e}")
