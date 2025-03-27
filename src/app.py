import streamlit as st
from scraper import get_news_articles
from sentiment import analyze_sentiment
from tts import generate_tts


st.set_page_config(page_title="News Summarization & Sentiment Analysis", layout="wide")

st.title("📰 News Summarization & Sentiment Analysis")


company_name = st.text_input("🔍 Enter Company Name:", placeholder="e.g., Tesla")

if st.button("Analyze"):
    if not company_name.strip():
        st.warning("⚠️ Please enter a valid company name!")
    else:
        
        articles = get_news_articles(company_name)

        if not articles:
            st.error("❌ No news articles found. Try another company.")
        else:
            results = []
            for article in articles:
                sentiment = analyze_sentiment(article["title"])
                results.append(
                    {
                        "Title": article["title"],
                        "Source": article["source"],
                        "Published At": article["publishedAt"],
                        "Sentiment": sentiment,
                        "Link": f"[Read More]({article['url']})",
                    }
                )

            
            st.subheader(f"📰 Latest News on {company_name}")
            st.table(results)

            
            summary_text = " ".join([a["title"] for a in articles])
            audio_file = generate_tts(summary_text)

            if audio_file:
                st.subheader("🎧 Listen to Summary")
                st.audio(audio_file)
            else:
                st.error("⚠️ Could not generate audio summary.")
