import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import pickle
import yaml
from pathlib import Path
from yaml.loader import SafeLoader
from datetime import datetime, timedelta
from collections import Counter
import re
import nltk
import io
from nltk.corpus import stopwords
import streamlit as st

# Custom helper modules
from helpers.sentiment import analyze_sentiment
from helpers.fake_news import detect_fake_news
from helpers.visualize import plot_sentiment_bar
from helpers.trend_visuals import plot_top_items_bar, generate_wordcloud
from helpers.forecasting import plot_forecasted_trends
from helpers.topic_modeling import extract_topics
from helpers.news_api import fetch_news
# Configuration
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# ------------------ Streamlit App Setup ------------------
st.set_page_config(page_title="TrendLENS", layout="centered")

#----------USER AUTHENTICATION----------------------
                      
# ------------------ Theme Toggle ------------------
theme = st.sidebar.selectbox("🌓 Choose Theme", ["Light", "Dark"])

#  Inject custom CSS based on theme
def set_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #0e1117;
                    color: #ffffff;
                }
                .css-18e3th9 {
                    background-color: #0e1117;
                }
                .stButton > button {
                    background-color: #262730;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #ffffff;
                    color: #000000;
                }
                .css-18e3th9 {
                    background-color: #ffffff;
                }
                .stButton > button {
                    background-color: #f0f0f0;
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

set_theme(theme)

st.title("Trend Lens – Social Media Sentiment analyzer and Trend Predictor")
st.markdown("Enter a social media post, tweet, or news headline below:")
# # ------------------ Sentiment Analysis ------------------
text = st.text_area("Text Input", height=150)

if st.button("🔍 Analyze"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            sentiment, sentiment_score = analyze_sentiment(text)
            label, fake_score = detect_fake_news(text)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Sentiment Result")
                st.success(f"**Sentiment:** {sentiment} ({sentiment_score:.2f})")
            with col2:
                st.subheader("📰 Fake News Detection")
                if label.upper() == 'FAKE':
                    st.error(f"**Label:** Fake News ({fake_score:.2f})")
                else:
                    st.info(f"**Label:** Real News ({fake_score:.2f})")

            st.subheader("📊 Sentiment Score Chart")
            fig = plot_sentiment_bar(sentiment, sentiment_score)
            st.pyplot(fig)
# ------------------ Trend Analysis ------------------
st.markdown("---")
st.header("📈 Trend Analysis – Hashtag & Keyword Extraction")

trend_input_method = st.radio(
    "Select Input Method",
    ("Manual Text Input", "Upload CSV File"),
    horizontal=True
)

texts = []
if trend_input_method == "Manual Text Input":
    user_input = st.text_area("Paste your social media posts/tweets (one per line)", height=200)
    if user_input.strip():
        texts = user_input.strip().split("\n")
elif trend_input_method == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload CSV file with a column named 'text'", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if "text" in df.columns:
                df.columns = [col.lower() for col in df.columns]
                texts = df["text"].dropna().tolist()
                st.success(f"Loaded {len(texts)} rows from CSV.")
            else:
                st.error("CSV must contain a 'text' column.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# NLP Utilities
def extract_hashtags(text_list):
    hashtags = []
    for text in text_list:
        hashtags += re.findall(r"#\w+", text.lower())
    return Counter(hashtags)

def extract_keywords(text_list):
    words = []
    for text in text_list:
        tokens = re.findall(r'\b\w+\b', text.lower())
        filtered = [word for word in tokens if word not in stop_words and len(word) > 2 and not word.startswith('#')]
        words.extend(filtered)
    return Counter(words)

# ------------------ Display Trends ------------------
hashtag_counts = Counter()
keyword_counts = Counter()

if texts:
    st.markdown("---")
    st.subheader("📌 Extracted Hashtags & Keywords")

    hashtag_counts = extract_hashtags(texts)
    keyword_counts = extract_keywords(texts)

    if hashtag_counts:
        st.markdown("**Top Hashtags:**")
        st.pyplot(plot_top_items_bar(hashtag_counts, "Top Hashtags", color='lightcoral'))
    else:
        st.info("No hashtags found.")

    if keyword_counts:
        st.markdown("**Top Keywords:**")
        st.pyplot(plot_top_items_bar(keyword_counts, "Top Keywords", color='lightgreen'))

        st.markdown("**Keyword Word Cloud:**")
        st.pyplot(generate_wordcloud(keyword_counts.keys()))
    else:
        st.info("No relevant keywords found.")
# ------------------ CSV Download Section for Forecasting ------------------

if hashtag_counts:
    # Generate the top 10 hashtags as daily data
    hashtag_data = [{
        'ds': (datetime(2025, 4, 1) + timedelta(days=i)).strftime('%Y-%m-%d'),
        'y': count,
        'hashtag': hashtag
    } for i, (hashtag, count) in enumerate(hashtag_counts.most_common(10))]

    # Create a DataFrame
    df_forecast = pd.DataFrame(hashtag_data)

    # Show preview in Streamlit
    st.markdown("**📋 Preview CSV Data:**")
    st.dataframe(df_forecast)

    # Convert DataFrame to CSV using StringIO
    csv_buffer = io.StringIO()
    df_forecast.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')  # Ensure it's encoded properly

    # Download button
    st.markdown("### 📥 Download Forecasting Data")
    st.download_button(
        label="Download CSV File",
        data=csv_bytes,
        file_name="forecasting_data.csv",
        mime="text/csv"
    )
# ------------------ Real-Time News from Extracted Hashtags ------------------
import requests

st.markdown("---")
st.header("📰News for Top Hashtags")

TOP_N = 10  # number of top hashtags to fetch news for

# Clean hashtags (remove '#' and skip short/irrelevant ones)
clean_hashtags = [tag.lstrip("#") for tag, _ in hashtag_counts.most_common(TOP_N) if len(tag) > 2]

if clean_hashtags:
    for tag in clean_hashtags:
        st.markdown(f"#### 🔎 News for #{tag}")

        # Build request URL
        url = f"https://newsapi.org/v2/everything?q={tag}&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"

        # Fetch news
        try:
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                if articles:
                    for i, article in enumerate(articles, 1):
                        st.write(f"**{i}. [{article['title']}]({article['url']})**")
                        st.caption(article["source"]["name"] + " | " + article["publishedAt"])
                else:
                    st.info("No recent articles found.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error fetching news: {e}")
else:
    st.info("No valid hashtags available to fetch news.")

    st.info("No valid hashtags available to fetch news.")

# ------------------ Sidebar – About Section ------------------
st.sidebar.title("📘 About TrendLENS")
st.sidebar.caption("App Version: 1.0.0")
st.sidebar.markdown("""
Trend Lens is an AI-powered application designed for analyzing social media posts, headlines, and content. It provides:
- Real-time **Sentiment Analysis**
- **Fake News Detection**
- **Trending Hashtag & Keyword Extraction**
- **Forecasting CSV Downloads**
- **Live News from Hashtags**

This tool helps users track public sentiment, detect misinformation, and discover trending topics.

---

### 🔗 Connect with Me
- 💼 [LinkedIn](https://www.linkedin.com/in/ankitkashyap01/)
- 💻 [GitHub](https://github.com/ankit8github)
- 📧 [ankit.kashyap0221@gmail.com](mailto:ankit.kashyap0221@gmail.com)

---

© 2025 **Ankit Kashyap**. All rights reserved.
""")



