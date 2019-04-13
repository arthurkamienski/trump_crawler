import requests
import json
import api_keys

def query_api(link):
    return requests.get(link).text

def news_list(text, number):
    news = json.loads(text)['articles']

    for article in news:
        del article['source']
        del article['content']

    return news[:number]

def build_link(keyword):
    return 'https://newsapi.org/v2/everything?' \
    f'q={keyword}&' \
    'sources=cnn&' \
    'sortBy=publishedAt&' \
    'apiKey=' + api_keys.news

def get_news(number=25, keyword='trump'):
    link = build_link(keyword)

    raw_text = query_api(link)

    return news_list(raw_text, number)

print(get_news())