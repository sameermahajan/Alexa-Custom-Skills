import json
import time
from botocore.vendored import requests

def lambda_handler(event, context):
    print (("event.dict.keys = {}").format(event.keys()))
    print (("event = {}").format(event))
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        url = event["context"]["System"]["apiEndpoint"] + '/v1/directives'
        payload = { 
                      "header": {
                          "requestId": event["request"]["requestId"]
                      },
                      "directive": {
                          "type":"VoicePlayer.Speak",
                          "speech":"<speak>This text is spoken while your skill processes the full response.</speak>"
                      }
                  }
        headers = {"Authorization":"Bearer " + event["context"]["System"]["apiAccessToken"], "Content-Type":"application/json"}
        print(("url = {} headers = {} payload = {}").format(url, headers, payload))
        ret = requests.post(url, json = payload, headers = headers)
        print (("post returned {} r.status_code = {} ret.text = {}").format(ret, ret.status_code, ret.text))
        time.sleep(2)
        return on_intent(event["request"], event["session"])
    return "Hello from Sameer's Lambda"

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    speech_output = "<speak> \
                        Welcome to Sameer's alexa tester. <break time='1s'/> \
                        Say listen followed by what you would like me to listen. \
                    </speak>"
    reprompt_text = "<speak> Please state what you would like to do now. </speak>"
    return build_response({}, build_speechlet_response(speech_output, reprompt_text, False))

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent["name"]
    if intent_name == "ListenIntent":
        return listen_user(intent)
        
def listen_user(intent):
    word = intent["slots"]["word"]["value"].lower()
    speech_output = ("<speak> I listened {}</speak>").format(word)
    reprompt_text = "<speak> Please state what you would like to do now. </speak>"
    return build_response({}, build_speechlet_response(speech_output, reprompt_text, False))
    
def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": reprompt_text
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
