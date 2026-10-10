# Real-Time Sentiment Analysis Demo

This project demonstrates a real-time Big Data pipeline that ingests a simulated stream of text (like social media comments), analyzes the sentiment (Positive/Negative/Neutral) on the fly, and stores it in a NoSQL database for live visualization.

It uses three core Big Data components:
1. **Apache Kafka:** For real-time message ingestion and buffering.
2. **TextBlob (NLP):** For processing and sentiment analysis.
3. **Elastic Stack (Elasticsearch & Kibana):** For fast NoSQL storage and live dashboard visualization.

## Prerequisites
* Docker and Docker Compose installed and running.
* Python 3.x installed.

## Setup Instructions

### 1. Start the Big Data Infrastructure
Open your terminal in this project folder and start the Docker containers. This will boot up Zookeeper, Kafka, Elasticsearch, and Kibana.

```bash
sudo docker compose up -d
```
*(Wait about 30-60 seconds for all services to fully start).*

### 2. Install Python Dependencies
If you haven't already, install the required Python libraries for the data stream and processing:

```bash
pip install -r requirements.txt
```

---

## Running the Demo

To run the demo, you will need two separate terminal windows open in this project folder.

### Step 1: Start the Data Stream (Terminal 1)
This script simulates a live stream of data (like Reddit comments or product reviews) and pushes them into an Apache Kafka topic.

```bash
python producer.py
```
*Leave this terminal running. You should see "Sent: [Review Text]" printing continuously.*

### Step 2: Start the Sentiment Processor (Terminal 2)
Open a new terminal window. This script acts as a Kafka consumer. It reads the live stream, calculates the sentiment score using NLP, and saves the categorized data into Elasticsearch.

```bash
python processor.py
```
*Leave this terminal running. You should see "Processed & Stored: [Sentiment] [Review Text]" printing continuously.*

---

## Viewing the Live Dashboard

With both Python scripts running, your pipeline is actively processing data. Now, visualize it.

1. Open your web browser and navigate to the Kibana UI: **http://localhost:5601**
2. In Kibana, open the main menu (top left) and go to **Stack Management** (scroll to the bottom).
3. Click on **Index Patterns** (under the Kibana section) and click **Create index pattern**.
4. In the "Index pattern name" field, type exactly: `sentiment_data` and click **Next step**.
5. In the "Time field" dropdown, select `timestamp` and click **Create index pattern**.
6. Open the main menu again and go to **Dashboard**.
7. Click **Create new dashboard**, then click **Create New** (or "Add a panel") and select **Pie Chart**.
8. Select the `sentiment_data` source.
9. On the right-side configuration panel:
   * Under **Buckets**, click **Add** and choose **Split slices**.
   * Aggregation: **Terms**
   * Field: **sentiment_label.keyword**
10. Click **Update** (bottom right). 
11. You will now see a live pie chart showing the real-time sentiment of your data stream! You can set the Kibana auto-refresh (top right corner, next to the date picker) to 2 seconds to watch it update automatically.

## Stopping the Project
When you are finished with the demo:
1. Press `Ctrl+C` in both terminal windows to stop the Python scripts.
2. Spin down the Docker containers by running:
```bash
sudo docker compose down
```


