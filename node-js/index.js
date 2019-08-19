/* global buildSpeechletResponse */

buildSpeechletResponse = (outputText, shouldEndSession) => {
    return {
        outputSpeech: {
            type: "PlainText",
            text: outputText
        },
        shouldEndSession: shouldEndSession
    }
}

/* global generateResponse */

generateResponse = (speechletResponse) => {
    return {
        version: "1.0",
        response: speechletResponse
    }
}

exports.handler = (event, context, callback) => {
    switch (event.request.type) {
        case "LaunchRequest":
            context.succeed(generateResponse(buildSpeechletResponse("Welcome to Sameer's Hello World. What is your first name?", false)));
            break;
        case "IntentRequest":
            switch (event.request.intent.name) {
                case "GreetHelloWorldIntent":
                    context.succeed(generateResponse(buildSpeechletResponse("Hello " + event.request.intent.slots.first_name.value, true)));
                    break;
            }
            break;
    }
}
