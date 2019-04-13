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
    user_tl = api.user_timeline(user, count=number)

    return [tweet.text for tweet in user_tl]

print(get_tweets())