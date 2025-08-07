from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
roberta_sentiment = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
def analyze_sentiment(text):
    result = roberta_sentiment(text)[0]
    label_map = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL",
        "LABEL_2": "POSITIVE"
    }
    label = label_map.get(result['label'], result['label'])
    return label, result['score'] 