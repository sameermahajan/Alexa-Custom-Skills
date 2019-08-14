Your skill some time might have to call a back end service that takes some time processing a request and giving a response. In this case you 
may want to invoke the service asynchronously. While waiting for its response, you may want to periodically send progressive response 
to alexa for keeping the user engaged in the dialogue.

## back end service

backend_service.py: It is hosted on lambda and faking some processing time by waiting for some time. You need to expose this service as an API endpoint using: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html#api-gateway-proxy-integration-create-lambda-backend


## Alexa Skill

alexa_skill.py is the alexa custom skill for python lambda.
InteractionModel.json is the interaction model  json for the above skill.
