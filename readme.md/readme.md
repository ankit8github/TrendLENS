📊 Trend Lens – Social Media Sentiment, Fake News, Trends & Forecasting

**Trend Lens** is a full-fledged AI-powered web app that analyzes social media posts, tweets, or headlines for **sentiment**, **fake news**, **hashtag trends**, and **forecasting**. It is built using Python and Streamlit and is aimed at providing real-time social insights for researchers, marketers, and analysts.

## 🚀 Features

### ✅ 1. Sentiment Analysis

* Classifies text into **Positive**, **Negative**, or **Neutral** sentiments.
* Uses transformer-based models like **RoBERTa**.
* Includes a **confidence score** for each sentiment class.
* Visualized using **bar charts**.

### ✅ 2. Fake News Detection

* Determines if the text is **Fake** or **Real** news.
* Uses a machine learning or transformer-based model.

### ✅ 3. Hashtag & Keyword Trend Extraction

* Extracts and visualizes trending **hashtags** and **keywords** from text or CSV files.
* Generates **bar charts** and **word clouds** to show frequency of hashtags/keywords.

### ✅ 4. Forecasting CSV Generator

* Extracts top 10 hashtags and generates a `forecasting_data.csv` file.
* File includes columns: `ds`, `y`, and `hashtag` to use in models like **Prophet** or **ARIMA**.
* Helps in time-series forecasting of hashtag popularity.

### ✅ 5. Real-Time News Feed

* Uses extracted top hashtags to fetch **live news articles** using the **NewsAPI**.
* Displays article title, source, time, and clickable URLs.

## 🗂️ File Structure

```
/trend-lens
│
├── app.py                     # Main Streamlit app
├── users.csv                  # (Optional) Stores login/signup data
│
├── helpers/
│   ├── sentiment.py           # Sentiment analysis logic
│   ├── fake_news.py           # Fake news detection
│   ├── visualize.py           # Sentiment visualization
│   ├── trend_visuals.py       # Word cloud & hashtag bar chart
│   ├── forecasting.py         # Forecasting CSV generator
│   └── news_api.py            # News fetching logic
│
├── forecasting_data.csv       # Generated dataset for trend forecasting
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/trend-lens.git
cd trend-lens
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Access the App

Go to your browser and open:
`http://localhost:8501`

---

## 🧪 Usage Instructions

1. **Input** your tweet, headline, or social media post.
2. Click **Analyze** to get:

   * Sentiment (Positive/Negative/Neutral)
   * Fake News detection (Fake/Real)
3. For CSV-based trend forecasting:

   * Upload a CSV file or let the app extract hashtags automatically.
   * Download `forecasting_data.csv` and use it in time-series models.
4. For live news:

   * Click on “Live News” to fetch top articles related to trending hashtags.

---

## 📚 Dependencies

* **Streamlit**
* **transformers**
* **torch**
* **pandas**
* **nltk**
* **matplotlib**
* **wordcloud**
* **requests**
* **re / datetime / collections**

## 👨‍💻 Author
**Ankit Kashyap**

* 💼 [LinkedIn](www.linkedin.com/in/ankitkashyap01)
* 💻 [GitHub](https://github.com/ankit8github)
* 📧 [Email.com](ankit.kashyap0221@gmail.com)

---

