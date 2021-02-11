#!/usr/bin/env python3
import tweepy, os, logging
from dotenv import load_dotenv
load_dotenv()


# Twitter bot to auto-RT select sports writers/reporters to curate a stream of sports news
# This twitter acount is https://twitter.com/BushLeagueSprts

logging.basicConfig(filename='bot.log', filemode='w', level=logging.WARNING)

class TweepyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

    def on_status(self, status):
        if not status.retweeted:
            try:
                self.api.retweet(status.id)
            except Exception as e:
                logging.error(e)

    def on_error(self, status_code):
        if status_code == 420:
            return False
        elif status_code == 327:
            return False


def return_api():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_KEY'), os.getenv('TWITTER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    return tweepy.API(auth)

def follow(users):
    # convert user IDs to strings
    # stream filter 'follow' takes array of string Ids, not integers.
    return [str(userId) for userId in users]

def run(api):
    streamListener = TweepyStreamListener(api)
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(follow=follow(api.friends_ids()))


if __name__ == "__main__":
    run(return_api())

