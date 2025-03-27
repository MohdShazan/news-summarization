import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set. Please check your .env file.")

def analyze_sentiment(text):
    """
    Analyzes sentiment of the given text using Hugging Face Inference API.
    Returns the sentiment label: "positive", "neutral", or "negative".
    """
    url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": text}

    try:
        response = requests.post(url, headers=headers, json=payload)

        
        if response.status_code != 200:
            return {
                "error": "Sentiment analysis failed",
                "status": response.status_code,
                "message": response.text
            }

        
        sentiment_data = response.json()

        if isinstance(sentiment_data, dict) and "error" in sentiment_data:
            return {
                "error": "API Error",
                "status": response.status_code,
                "message": sentiment_data.get("error", "Unknown error")
            }

        
        if not isinstance(sentiment_data, list) or len(sentiment_data) == 0 or not isinstance(sentiment_data[0], list):
            return {"error": "Invalid API response format", "status": 500}


        sentiment_scores = sentiment_data[0]
        highest_score_label = max(sentiment_scores, key=lambda x: x["score"])["label"]

        
        sentiment_mapping = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }

        
        return {"sentiment": sentiment_mapping.get(highest_score_label, "Unknown")}

    except requests.exceptions.RequestException as e:
        return {
            "error": "Request failed",
            "status": "500",
            "message": str(e)
        }
