import json
import time

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_model.services.directive import (
    SendDirectiveRequest, Header, SpeakDirective)

word_list = ['word', 'apple', 'ball']

class OnLaunchHandler(AbstractRequestHandler):
    """Handler for Skill Launch"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        i = int(time.time() % len(word_list))

        # Get any existing attributes from the incoming request
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['word'] = word_list[i]
        speech_text = ("Welcome to Sameer's spelling tutor. Please spell the word {}.").format(session_attr['word'])
        reprompt_text = "Please state what you would like to do now."
        return handler_input.response_builder.speak(speech_text).ask(reprompt_text).response

class SpellingHandler(AbstractRequestHandler):
    """Handler for WordSpellingIntent Launch"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("WordSpellingIntent")(handler_input) or
                ask_utils.is_intent_name("AppleSpellingIntent")(handler_input) or
                ask_utils.is_intent_name("BallSpellingIntent")(handler_input))

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        speech_text = ("you spelt it incorrectly. The correct spelling is {}").format(get_word_spelling(session_attr['word']))

        if "word" in session_attr:
            if ((session_attr['word'] == 'word' and ask_utils.is_intent_name("WordSpellingIntent")(handler_input)) or
                (session_attr['word'] == 'apple' and ask_utils.is_intent_name("AppleSpellingIntent")(handler_input)) or
                (session_attr['word'] == 'ball' and ask_utils.is_intent_name("BallSpellingIntent")(handler_input))):
                speech_text = ("you spelt it correctly as {}").format(get_word_spelling(session_attr['word']))

        request_id_holder = handler_input.request_envelope.request.request_id
        directive_header = Header(request_id=request_id_holder)
        speech = SpeakDirective(speech="Ok, give me a minute")
        directive_request = SendDirectiveRequest(
        header=directive_header, directive=speech)

        directive_service_client = handler_input.service_client_factory.get_directive_service()
        directive_service_client.enqueue(directive_request)
        # Adding a 2 second sleep for testing
        time.sleep(2)
        return handler_input.response_builder.speak(speech_text).response

def get_word_spelling(word):
    word_spelling = ""

    for l in word:
        word_spelling += l + ' '

    return word_spelling
sb = CustomSkillBuilder(api_client=DefaultApiClient())

# Register intent handlers
sb.add_request_handler(OnLaunchHandler())
sb.add_request_handler(SpellingHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
