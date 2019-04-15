#!/usr/bin/env python3

import requests
import json
import api_keys
from datetime import datetime
import matplotlib.pyplot as plt

# query news api and return the content of the request
def query_api(link):
    return requests.get(link).text

# parse raw json data from the api and return a list of articles 
def news_list(text):
    news = json.loads(text)['articles']

    # unecessary information
    for article in news:
        del article['source']

    return news

# build the link (string) to query the API based on a search keyword and number
# of results
def build_link(keyword, number):
    return 'https://newsapi.org/v2/everything?' \
    f'q={keyword}&' \
    'sources=cnn&' \
    'sortBy=publishedAt&' \
    f'pageSize={number}&' \
    'language=en&' \
    'apiKey=' + api_keys.news

# wraps the links building, api querying and parsing funcionts
def get_news(number=25, keyword='trump'):
    link = build_link(keyword, number)

    raw_text = query_api(link)

    return news_list(raw_text)

# calculates time difference between now and the time of the post
# returns a string corresponding to the time difference truncated
# to the greatest unit
def time_diff(date):
    diff = datetime.utcnow() - date
    time = str(diff.days) + ' days ago'

    if diff.days == 1:
        time = '1 day ago'
    elif diff.days == 0:
        hours = diff.seconds//3600
        time = str(hours) + ' hours ago'
        
        if hours == 1:
            time = '1 hour ago'
        elif hours == 0:
            minutes = diff.seconds//60
            time = str(minutes) + ' minutes ago'

            if minutes == 1:
                time = '1 minute ago'
            elif minutes == 0:
                time = 'just now'

    return time

# turns the list of news into HTML code to be used on the webpage
# each article is a cell div inside a wrapper feed div
def print_html(news):

    print("<div class='feed' id='cnn-feed'>")

    for i, n in enumerate(news):
        # for Javascript DOM
        html_id = 'news' + str(i)

        url = n['url']
        image= n['urlToImage']
        title = n['title']
        author = n['author']
        content = n['content']
        date = datetime.strptime(n['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')


        date = time_diff(date)

        text = n['description']

        print(f"""
            <div class='cell' id='{html_id}'>
                <div class='cell-img'>
                    <a href="{url}" target='_blank' class='article-title'>
                        <img src="{image}">
                    </a>
                </div>
                <div class='cell-content'>
                    <div class='cell-header'>
                        <a class='article-title' href="{url}" target='_blank'>
                            <span class='headline'>{title}</span> <br>
                            <span class='author'>{author}</span> <span class='time'>{date}</span>
                        </a>
                    </div>
                    <div class='cell-text' id='{html_id}-text'>
                        {text}
                    </div>
                    <div class='cell-info' id='{html_id}-info'>
                        <a href="{url}" target='_blank'>
                            Original Post
                        </a> ||
                        <span class='info-button' onclick="makediv('{html_id}', 'cnn');">Further Info</span>
                    </div>
                    <div id='{html_id}-additional' class='additional'>
                        {content} <a href="{url}" target='_blank'>Read more on CNN...</a>
                    </div>
                </div>
            </div>
        """)

    print("</div>")



if __name__ == '__main__':
    news = get_news()
    print_html(news)