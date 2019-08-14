Your skill some time might have to call a back end service that takes some time processing a request and giving a response. In this case you 
may want to invoke the service asynchronously. While waiting for its response, you may want to periodically send progressive response 
to alexa for keeping the user engaged in the dialogue.

## back end service

backend_service.py: It is faking some processing time by waiting for some time.
