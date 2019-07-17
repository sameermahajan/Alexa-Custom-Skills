def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    return "Hello from Sameer's Lambda"

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    speech_output = "<speak> \
                        Welcome to Sameer's lambda based alexa custom skill for repeating a user. <break time='1s'/> \
                        What would you like to do now? <break time='1s'/> \
                    </speak>"
    reprompt_text = "<speak> Please state what you would like to do now. </speak>"
    return build_response({}, build_speechlet_response("welcome or help", speech_output, reprompt_text, False))

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent["name"]
    msg = ""
    if intent_name == "repeat":
        return repeat_user(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
	    msg = "<speak> \
                    Thank you for using Sameer's lambda based alexa custom skill for repeating a user. \
                    <break time='1s'/> See you next time \
        </speak>"
    return build_response({}, build_speechlet_response("stopping or canceling", msg, "", True))

def repeat_user(intent):
    speech_output = "<speak> Did you just say " + intent["slots"]["phrase"]["value"] + " ? </speak>"
    reprompt_text = "<speak> Please state what you would like to do now. </speak>"
    return build_response({}, build_speechlet_response("repeating user", speech_output, reprompt_text, False))
    
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": title
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
