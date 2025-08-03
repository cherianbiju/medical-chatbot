# chatbot_app/modules/analytics.py

import os
import csv
from collections import Counter

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "chat_logs.csv")

def log_interaction(user_input, bot_response, sentiment="neutral"):
    # Append to CSV
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_input, bot_response, sentiment])

def get_summary():
    if not os.path.exists(LOG_FILE):
        return {
            "total_queries": 0,
            "top_keywords": [],
            "sentiment_distribution": {}
        }

    queries = []
    sentiments = []

    with open(LOG_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                queries.append(row[0])
                sentiments.append(row[2])

    # Basic keyword frequency
    words = [word.lower() for q in queries for word in q.split()]
    top_keywords = Counter(words).most_common(5)
    sentiment_count = Counter(sentiments)

    return {
        "total_queries": len(queries),
        "top_keywords": top_keywords,
        "sentiment_distribution": sentiment_count
    }
