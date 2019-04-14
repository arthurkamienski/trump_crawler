#!/usr/bin/env python3

import tweepy
import api_keys

def make_auth():
    keys = api_keys.twitter

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    return auth

def get_tweets(user='realDonaldTrump', number=25):
    auth = make_auth()

    api = tweepy.API(auth)
    user_tl = api.user_timeline(user, count=number, tweet_mode='extended',include_entities=True)

    return [tweet for tweet in user_tl]

def print_html():

    tweets = get_tweets()

    print("<div class='feed'>")

    for tweet in tweets:
        print(
        f"""
            <div class='cell' onclick="window.open('https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}');" style="cursor: pointer;">
                <div class='cell-img'>
                    <a class='twitter-profile' href="https://twitter.com/{tweet.user.screen_name}" target="_blank">
                        <img src="{tweet.user.profile_image_url}">
                    </a>
                </div>
                <div class='cell-content'>
                    <div class='cell-header'>
                        <a class='twitter-profile' href="https://twitter.com/{tweet.user.screen_name}" target="_blank">
                            {tweet.user.name} <span class='username'>@{tweet.user.screen_name}</span> {tweet.created_at}
                        </a>
                    </div>  
                    <div class='cell-text'>
                        {tweet.full_text}
                    </div>
                </div>
            </div>
        """
        )

    print("</div>")

if __name__ == '__main__':
    print_html()