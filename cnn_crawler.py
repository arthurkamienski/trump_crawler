import requests
import json

def get_key():
    with open('cnn_api_key.txt', 'r') as key_file:
        key = key_file.readline()
    return key

def query_api(link):
    return requests.get(link).text

def news_list(text):
    news = json.loads(text)['articles']

    for article in news:
        del article['source']
        del article['content']

    return news

def build_link(keyword='trump'):
    return 'https://newsapi.org/v2/everything?' \
    f'q={keyword}&' \
    'sources=cnn&' \
    'sortBy=publishedAt&' \
    'apiKey=' + get_key()


def main():
    articles_num = 25

    link = build_link()

    raw_text = query_api(link)

    return news_list(raw_text)

if __name__ == '__main__':
    lists = main()

    print(lists[:25])