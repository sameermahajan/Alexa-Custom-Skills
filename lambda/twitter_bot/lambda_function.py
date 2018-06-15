# Import the necessary methods from "twitter" library

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

from collections import OrderedDict

# Variables that contains the user credentials to access Twitter API 
# Get these from: https://apps.twitter.com/
# You can read more details about it at: http://socialmedia-class.org/twittertutorial.html

ACCESS_TOKEN = '...'
ACCESS_SECRET = '...'
CONSUMER_KEY = '...'
CONSUMER_SECRET = '...'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	
def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    return "Hello from Sameer's Lambda"
    
def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    session_attributes = {}
    card_title = ""
    speech_output = "<speak> \
                        Welcome to Sameer's lambda based alexa custom skill for twitter. <break time='1s'/> \
                        What would you like to do now? <break time='1s'/> \
                        get trends for places <break time='1s'/> \
                        get recent tweets <break time='1s'/> \
                        get tweets on topic <break time='1s'/> \
                        get tweets from handle <break time='1s'/> \
                        get user details \
                    </speak>"
    reprompt_text = "<speak> Please state what you would like to do now. </speak>"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    msg = ""
    if intent_name == "GetLocationTrends":
        return get_location_trends(intent)
    elif intent_name == "GetTweetsOnTopic":
        return get_topic_tweets(intent)
    elif intent_name == 'GetTweetsFromHandle':
        return get_handle_tweets(intent)
    elif intent_name == "GetRecentTweets":
        return get_recent_tweets(intent)
    elif intent_name == "GetUserDetails":
        return get_user_details(intent)
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
		msg =   "<speak> \
                    Thank you for using Sameer's lambda based alexa custom skill for twitter. <break time='1s'/> \
                    See you next time \
                </speak>"
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    return build_response({}, build_speechlet_response("", msg, "", True))
        
def get_location_trends(intent):
    try:
        location = intent["slots"]["location"]["value"]
        count = int(intent["slots"]["count"]["value"])
        twitter = Twitter(auth=oauth)
        world_trends = twitter.trends.available(_woeid=1)
        woeid = 2295412
    
        for trend in world_trends:
            if trend['name'] == location:
	            woeid = trend['woeid']

        trends = twitter.trends.place(_id = woeid)[0]['trends']

        # Sort descending based on tweet_volume

        trends_dict = {}
	
        for trend in trends:
            if trend['tweet_volume']:
                trends_dict[trend['name']] = int(trend['tweet_volume'])

        d_descending = OrderedDict(sorted(trends_dict.items(), key=lambda x: (-x[1], x[0])))
    
        msg = "<speak> " + str(count) + " trends for " + location + " are "

        for key in d_descending:
            count -= 1
            msg += key + " <break time='1s'/> "
            if count <= 0:
                break

        msg += "</speak>"
        return build_response({}, build_speechlet_response("", msg, "", True))
    except:
        pass
    return get_welcome_response()

def get_topic_tweets(intent):
    try:
        count = int(intent["slots"]["count"]["value"])
        topic = intent["slots"]["topic"]["value"]
        twitter = Twitter(auth=oauth)
        tweets = twitter.search.tweets(q=topic, result_type='recent', count=count)['statuses']
	
        msg = "<speak> recent " + str(count) + " tweets on " + topic + " are <break time='1s'/>"
        for tweet in tweets:
            count -= 1
            try:
                msg += " user name is " + tweet['user']['name']
                msg += " tweet is " + tweet['text'] + " <break time='1s'/> "
            except:
                continue
            if count <= 0:
                break

        msg += "</speak>"
        return build_response({}, build_speechlet_response("", msg, "", True))
    except:
        pass
    return get_welcome_response()

def get_handle_tweets(intent):
    try:
        handle = intent["slots"]["handle"]["value"]
        count = int(intent["slots"]["count"]["value"])
        twitter = Twitter(auth=oauth)
        tweets = twitter.statuses.user_timeline(screen_name=handle)

        msg = "<speak> " + str(count) + " tweets from " + handle + " are <break time='1s'/>"

        for tweet in tweets:
            count -= 1
            msg += "tweet is " + tweet['text'] + " <break time='1s'/> "
            # print (tweet['text'].encode("utf-8"))
            if count <= 0:
                break

        msg += "</speak>"
        return build_response({}, build_speechlet_response("", msg, "", True))
    except:
        pass
    return get_welcome_response()

def get_recent_tweets(intent):
    try:
        count = int(intent["slots"]["count"]["value"])

        # Initiate the connection to Twitter Streaming API

        twitter_stream = TwitterStream(auth=oauth)

        # Get a sample of the public data following through Twitter

        iterator = twitter_stream.statuses.sample()
    
        msg = "<speak> recent " + str(count) + " tweets are <break time='1s'/>"
        for tweet in iterator:
            count -= 1
            try:
                if 'text' in tweet: # only messages contains 'text' field is a tweet
                    msg += "user name is " + tweet['user']['name']
                    msg += "tweet is " + tweet['text'] + " <break time='1s'/> "
            except:
                continue
            if count <= 0:
                break
        
        msg += "</speak>"
        return build_response({}, build_speechlet_response("", msg, "", True))
    except:
        pass
    return get_welcome_response()

def get_user_details(intent):
    try:
        handle = intent["slots"]["handle"]["value"]
        twitter = Twitter(auth=oauth)
        users = twitter.users.search(q = handle)
        msg = "<speak> users for handle " + handle + " are <break time='1s'/>"
    
        for user in users:
            msg += " name is " + user['name'] + " having " + str(user['followers_count']) + " followers following " + str(user['friends_count']) + " handles "
            msg += " with " + str(user['statuses_count']) + " tweets located in " + user['location'] + " with " + str(user['favourites_count'])
            msg += " likes and joined on " + str(user['created_at']) + " <break time='1s'/> "
    
        msg += "</speak>"
        return build_response({}, build_speechlet_response("", msg, "", True))
    except:
        pass
    return get_welcome_response()

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "SSML",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }