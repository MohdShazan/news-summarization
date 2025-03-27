import os
import requests
from dotenv import load_dotenv


load_dotenv()
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def get_news_articles(query):
    """
    Fetches news articles related to a company using GNews API and removes duplicates.
    """
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "token": GNEWS_API_KEY,
        "lang": "en",
        "sortby": "publishedAt",
        "max": 5
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch news", "status": response.status_code}

    data = response.json()
    articles = data.get("articles", [])

    if not articles:
        return {"error": "No articles found", "status": 404}

    
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        title = article.get("title")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append({
                "title": title,
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "publishedAt": article.get("publishedAt"),
                "description": article.get("description")
            })

    return unique_articles
