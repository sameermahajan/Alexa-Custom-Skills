import asyncio
from botocore.vendored import requests
import time

def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event)
    return "Hello from Sameer's Lambda"

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    speech_output = "<speak> \
                        Welcome to Sameer's lambda based alexa custom skill for async loop. <break time='1s'/> \
                        What is your first name? <break time='1s'/> \
                    </speak>"
    reprompt_text = "Please state what you would like to do now."
    return build_response({}, build_speechlet_response(speech_output, reprompt_text, False))

def on_intent(intent_request, event):
    intent = intent_request["intent"]
    intent_name = intent["name"]
    if intent_name == "SayHelloIntent":
        return on_say_hello(intent["slots"]["first_name"]["value"], event)
        
def on_say_hello(first_name, event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(progressive_response_loop(first_name, event))
    loop.close()
    speech_output = "<speak> " + result + " </speak>"
    return build_response({}, build_speechlet_response(speech_output, "some reprompt text", True))

async def api_call(first_name):
    loop = asyncio.get_event_loop()
    # it is a lambda / back end call that takes  20 sec
    future = loop.run_in_executor(None, requests.get, '<your api endpoint> + '?name=' + first_name)
    response = await future
    print (("response = {}").format(response))
    return str(response.text)

async def progressive_response_loop(first_name, event):
    back_end_call = asyncio.ensure_future(api_call(first_name))

    while not back_end_call.done():
        # send progressive response
        url = event["context"]["System"]["apiEndpoint"] + '/v1/directives'
        payload = { 
                      "header": {
                          "requestId": event["request"]["requestId"]
                      },
                      "directive": {
                          "type":"VoicePlayer.Speak",
                          "speech":"<speak>Please wait while I fetch the results.</speak>"
                      }
                  }
        headers = {"Authorization":"Bearer " + event["context"]["System"]["apiAccessToken"], "Content-Type":"application/json"}
        print(("url = {} headers = {} payload = {}").format(url, headers, payload))
        ret = requests.post(url, json = payload, headers = headers)
        print (("post returned {} r.status_code = {} ret.text = {}").format(ret, ret.status_code, ret.text))
        print ('looping till back end call completes ' + str(time.time()))
        await asyncio.sleep(5)

    print ('back end call is  complete. get results.')
    result = back_end_call.result()
    print (("result = {}").format(result))
    return result
    
def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
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
