#!/usr/bin/env python3

import requests
import json
import api_keys

def query_api(link):
    return requests.get(link).text

def news_list(text):
    news = json.loads(text)['articles']

    for article in news:
        del article['source']
        del article['content']

    return news

def build_link(keyword, number):
    return 'https://newsapi.org/v2/everything?' \
    f'q={keyword}&' \
    'sources=cnn&' \
    'sortBy=publishedAt&' \
    f'pageSize={number}&' \
    'apiKey=' + api_keys.news

def get_news(number=25, keyword='trump'):
    link = build_link(keyword, number)

    raw_text = query_api(link)

    return news_list(raw_text)

def print_html():

    news = get_news()

    print("<div class='feed'>")

    for n in news:
        url = n['url']
        image= n['urlToImage']
        title = n['title']
        author = n['author']
        date = n['publishedAt']
        text = n['description']

        print(f"""
            <div class='cell' onclick="window.open('{url}');" style="cursor: pointer;">
                <div class='cell-img'>
                    <img src="{image}">
                </div>
                <div class='cell-content'>
                    <div class='cell-header'>
                        <b>{title}</b><br>
                        {author} - {date}
                    </div>
                    <div class='cell-text'>
                        {text}
                    </div>
                </div>
            </div>
        """)

    print("</div>")

if __name__ == '__main__':
    print_html()