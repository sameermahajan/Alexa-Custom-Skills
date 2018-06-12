import logging
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
# Get these from: https://apps.twitter.com/
# You can read more details about it at: http://socialmedia-class.org/twittertutorial.html
ACCESS_TOKEN = '...'
ACCESS_SECRET = '...'
CONSUMER_KEY = '...'
CONSUMER_SECRET = '...'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

@ask.launch
def welcome():
    return question(render_template('welcome'))

@ask.intent("ReadTweetsIntent")
def read_tweets(count):
    c = int(count)
    msg = ""
    for tweet in iterator:
        c -= 1
        try:
            if 'text' in tweet: # only messages contains 'text' field is a tweet
                msg += "user name is " + tweet['user']['name']
                msg += "tweet is " + tweet['text']
        except:
            continue
       
        if c <= 0:
            break

    tweets = render_template('summary', count=count, msg=msg)
    return question(tweets)
	
if __name__ == '__main__':
    app.run(debug=True)