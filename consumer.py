import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialisation d'Elasticsearch (version 7.x) et du modèle NLP VADER
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
analyzer = SentimentIntensityAnalyzer()

# Configuration du Consumer Kafka
consumer = KafkaConsumer(
    'social-media-stream',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🧠 NLP Consumer is listening to Kafka and processing data...")

try:
    for message in consumer:
        raw_data = message.value
        text_to_analyze = raw_data['text']
        
        # Inference NLP (Calcul des scores de sentiment)
        scores = analyzer.polarity_scores(text_to_analyze)
        compound_score = scores['compound']
        
        # Classification du sentiment selon le score global
        if compound_score >= 0.05:
            sentiment = "Positive"
        elif compound_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        # Enrichissement du dictionnaire de données initial
        enriched_data = {
            **raw_data,
            "sentiment": sentiment,
            "sentiment_score": compound_score,
            "pos_score": scores['pos'],
            "neg_score": scores['neg']
        }
        
        # Indexation (sauvegarde) dans Elasticsearch
        res = es.index(index="sentiment-analysis-index", document=enriched_data)
        print(f"✅ Processed & Indexed f Elastic: [{sentiment}] -> {text_to_analyze[:40]}...")

except KeyboardInterrupt:
    print("🛑 Consumer stopped.")