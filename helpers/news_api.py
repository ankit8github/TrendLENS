import requests

def fetch_news(api_key, query, language='en', page_size=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={page_size}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return [article["title"] for article in articles]
    else:
        return []
