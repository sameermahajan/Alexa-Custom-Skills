# Progressive Response

Alexa skill can send progressive responses to keep the user engaged while the skill prepares a full response to the user's request.

You can read more details at: https://developer.amazon.com/docs/custom-skills/send-the-user-a-progressive-response.html

I could not get my python code working using the low level http specification given above initially and I had posted my question on the forum at: 
https://forums.developer.amazon.com/questions/211582/progressive-response-not-working-with-low-level-ht.html

**Note there is an update to it posted below [Using Pogressive Response without SDK](https://github.com/sameermahajan/Alexa-Custom-Skills/blob/master/ProgressiveResponse/README.md#using-pogressive-response-without-sdk)**

However I could get it working with Python ASK SDK. To use the SDK, you need to create deployment package if you want to use lambda for 
your skill, as python runtimes provided by lambda do not include this SDK. To do this (say on an ubuntu EC2 instance) do

```
mkdir my-lambda-deployment-package
cd my-lambda-deployment-package
sudo pip3 install -t ./ ask-sdk
copy the lambda_handler.py provided in this repo to this folder
zip -r ../my-lambda-deployment-package.zip .
cd ..
```

## Copy the deployment package to s3

```
aws s3 cp my-lambda-deployment-package.zip s3://myfirst-alexa-skill/my-lambda-deployment-package.zip
```

upload this package to your lambda and set the Handler to lambda_handler.lambda_handler

## Using Pogressive Response without SDK

You can use lambda_handler_without_sdk.py from this repo to send progressive response without SDK. Please follow the discussion in the forum post mentioned above for details.
