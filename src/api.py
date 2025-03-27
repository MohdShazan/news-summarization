from fastapi import FastAPI, HTTPException
from scraper import get_news_articles
from sentiment import analyze_sentiment

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the AI News API 🚀"}

@app.get("/news")
def fetch_news(company: str):
    try:
        news = get_news_articles(company)

        if not news or "error" in news:
            raise HTTPException(status_code=404, detail="No news articles found or API error.")

        return {"company": company, "articles": news}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/sentiment")
def fetch_sentiment(text: str):
    try:
        sentiment = analyze_sentiment(text)
        return {"text": text, "sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment Analysis Error: {str(e)}")
