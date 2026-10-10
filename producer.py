import time
import json
from kafka import KafkaProducer
from newsapi import NewsApiClient

# ==========================================
# PASTE YOUR NEWS API KEY HERE
NEWS_API_KEY = 'cade7cf61c20448a8a3c2cea4c9a422d' 
# ==========================================

# Connect to our Docker Kafka (using port 29092 as defined in docker-compose)
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize News API
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

print("Starting to fetch live news headlines... (Press Ctrl+C to stop)")

def fetch_and_send():
    try:
        # Fetch the top headlines for technology
        top_headlines = newsapi.get_top_headlines(category='technology', language='en')
        
        articles = top_headlines.get('articles', [])
        
        for article in articles:
            title = article.get('title')
            if title:
                data = {
                    "text": title,
                    "timestamp": int(time.time() * 1000)
                }
                
                # Send to Kafka
                producer.send('live_reviews', value=data)
                print(f"Sent News: {title}")
                time.sleep(1) # Send 1 per second
                
    except Exception as e:
        print(f"Error fetching news: {e}")

try:
    while True:
        fetch_and_send()
        print("Waiting 60 seconds before checking for new headlines...")
        time.sleep(60) 

except KeyboardInterrupt:
    print("\nStreaming stopped.")
