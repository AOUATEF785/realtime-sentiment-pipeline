import time
import json
import random
from kafka import KafkaProducer

# Configuration du Producer Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'social-media-stream'

# Simulation de phrases d'utilisateurs (Feedbacks, Tweets, News)
sample_reviews = [
    "I absolutely love the new features of this AI tool! Game changer.",
    "Horrible customer service, I've been waiting for hours. Waste of time.",
    "It's okay, not bad but nothing special either.",
    "Wow, this platform makes my data science work 10x faster! Highly recommend.",
    "Extremely disappointed with the latest software update, it keeps crashing.",
    "The data processing pipeline is incredibly fast and efficient.",
    "Worst experience ever. The system is lagging and completely unstable."
]

print("🚀 Starting Kafka Producer... Press Ctrl+C to stop.")

try:
    while True:
        data = {
            "timestamp": int(time.time() * 1000),
            "source": random.choice(["Twitter", "Reddit", "News"]),
            "text": random.choice(sample_reviews),
            "user_followers": random.randint(10, 50000)
        }
        
        # Envoi au topic Kafka
        producer.send(TOPIC_NAME, value=data)
        print(f"📡 Sent to Kafka: {data['text'][:50]}...")
        
        # Délai de 0.5 seconde entre chaque message pour simuler un flux continu
        time.sleep(0.5) 

except KeyboardInterrupt:
    print("🛑 Producer stopped.")