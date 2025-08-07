from transformers import pipeline

fake_news_model = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")

def detect_fake_news(text):
    result = fake_news_model(text)[0]
    return result['label'], result['score']
