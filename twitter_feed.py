#!/usr/bin/env python3

import tweepy
import api_keys
from datetime import datetime
import re

# runs OAuth and returns corresponding authorization based on API keys
def make_auth():
    keys = api_keys.twitter

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    return auth

# Querries Twitter API and returns a list of tweets (Status objects)
def get_tweets(user='realDonaldTrump', number=25):
    auth = make_auth()

    api = tweepy.API(auth)
    user_tl = api.user_timeline(user, count=number, tweet_mode='extended',include_entities=True)

    return [tweet for tweet in user_tl]

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

# creates html for a retweet (slightly different from a tweet)
def make_retweet_html(tweet):
    time = time_diff(tweet.created_at)
    text = link_text(tweet)

    return f"""
            <hr>
            <b>RETWEETED FROM</b>

            <div class='cell'>
                <div class='cell-img'>
                    <a class='twitter-profile' href='https://twitter.com/{tweet.user.screen_name}' target="_blank">
                        <img src="{tweet.user.profile_image_url}">
                    </a>
                </div>
                <div class='cell-content'>
                    <div class='cell-header'>
                        <a class='twitter-title' href="https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}" target="_blank">
                            <span class='username'>{tweet.user.name}</span> <span class='screen-name'>@{tweet.user.screen_name}</span><span class='time'>{time} </span>
                        </a>
                    </div>  
                    <div class='cell-text'>
                        {text}
                    </div>
                    <div class='cell-info'>
                        <a href="https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}" target='_blank'>
                            Original Post
                        </a>
                    </div>
                    <div>
                        &#8635; Retweeted <b> {tweet.retweet_count} </b> times ||
                        &#11088; Favorited <b> {tweet.favorite_count} </b> times
                    </div>
                </div>
            </div>
        """

# creates the html for the tweet
def make_tweet_html(tweet, html_id):
    time = time_diff(tweet.created_at)


    try:
        favorite = tweet.retweeted_status.favorite_count

        text = link_text(tweet.retweeted_status)
        
        retweet = f"""
            <b> (Retweeted from 
            <a class='twitter-profile' href='https://twitter.com/{tweet.retweeted_status.user.screen_name}' target="_blank">
                @{tweet.retweeted_status.user.screen_name}
            </a>)</b>
        """
    except AttributeError:
        retweet = ''
        favorite = tweet.favorite_count
        text = link_text(tweet)

    additional = make_additional(tweet)

    return f"""
            <div class='cell' id='{html_id}'>
                <div class='cell-img'>
                    <a class='twitter-profile' href='https://twitter.com/{tweet.user.screen_name}' target="_blank">
                        <img src="{tweet.user.profile_image_url}">
                    </a>
                </div>
                <div class='cell-content'>
                    <div class='cell-header'>
                        <a class='twitter-title' href="https://twitter.com/{tweet.user.screen_name}" target="_blank">
                            <span class='username'>{tweet.user.name}</span> <span class='screen-name'>@{tweet.user.screen_name}</span> {retweet}<span class='time'>{time} </span>
                        </a>
                    </div>  
                    <div class='cell-text' id='{html_id}-text'>
                        {text}
                    </div>
                    <div class='cell-info' id='{html_id}-info'>
                        <a href="https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}" target='_blank'>
                            Original Post
                        </a> || 
                        <span class='info-button' onclick="makediv('{html_id}', 'twitter');">Further Info</span>
                    </div>
                    <div id='{html_id}-additional' class='additional'>
                        &#8635; Retweeted <b> {tweet.retweet_count} </b> times <br>
                        &#11088; Favorited <b> {favorite} </b> times <br>
                        
                        {additional}
                    </div>
                </div>
            </div>
        """

# creates links in the tweet text to other tweets/users
def link_text(tweet):
    text = tweet.full_text

    for m in tweet.entities['user_mentions']:
        screen_name = m['screen_name']
        name = m['name']

        pattern = re.compile(f"@{screen_name}", re.IGNORECASE)
        text = pattern.sub(f"<a href='https://twitter.com/{screen_name}' target='_blank'>@{screen_name}</a>",
         text)

    for u in tweet.entities['urls']:
        url = u['url']

        text = text.replace(url, f"<a href='{url}' target='_blank'>{url}</a>")

    return text

# Creates the additional information that will be hidden at first
def make_additional(tweet):
    additional = ''

    if len(tweet.entities['user_mentions']) > 0:
        additional += '<hr><b> User Mentions: </b><br>'

        for m in tweet.entities['user_mentions']:
            screen_name = m['screen_name']
            name = m['name']

            additional += f"""
                {name} <a href='https://twitter.com/{screen_name}' target='_blank'>@{screen_name}</a><br>
            """
    
    if len(tweet.entities['urls']) > 0:
        additional += '<hr><b> URLs: </b><br>'

        for u in tweet.entities['urls']:
            url = u['url']

            additional += f"""
            <a href='{url}' target='_blank'>{url}</a><br>
            """

    try:
        additional += make_retweet_html(tweet.retweeted_status)
    except AttributeError:
        pass

    return additional

# turns the list of tweets into HTML code to be used on the webpage
# each tweet is a cell div inside a wrapper feed div
def print_html(tweets):
    print("<div class='feed' id='twitter-feed'>")

    for i, tweet in enumerate(tweets):
        # for Javascript DOM
        html_id = 'tweet' + str(i)

        print(
            make_tweet_html(tweet, html_id)
        )

    print("</div>")

if __name__ == '__main__':
    tweets = get_tweets()
    print_html(tweets)