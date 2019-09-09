This is easy to refer compilation of information around alexa custom skill gathered while working on multiple projects.

Custom Skills can be either hosted on AWS lambda or they can be on prem  using flask-ask. 

## Folder 'lambda' 

has lambda based skills in python.

## Folder 'flask-ask'

has flask-ask based skills.

## Folder 'node-js'

has lambda based skill in node.js.

## Folder 'ProactiveEvents'

describes how to send async notifications / events to alexa using python in lambda.

## Folder 'ProgressiveResponse'

describes how to send progressive response to alexa using python in lambda.

## Folder 'async-loop'

describes how to make an async call, wait for the response, send progressive response until the final response using python in lambda.

## Some other useful blogs

Here are some other useful blogs:

- Alexa Custom Skill Life Cycle: https://medium.com/@sameermahajan/alexa-custom-skill-life-cycle-d26417ae36d9
- add another user to use your dev skill: https://developer.amazon.com/blogs/alexa/post/Tx2EN8P2AHAHO6Y/how-to-add-beta-testers-to-your-skills-before-you-publish
- improve discovery of your skill using CanFulfillIntentRequest: 
  * https://developer.amazon.com/blogs/alexa/post/352e9834-0a98-4868-8d94-c2746b794ce9/improve-alexa-skill-discovery-and-name-free-use-of-your-skill-with-canfulfillintentrequest-beta
  * https://developer.amazon.com/docs/custom-skills/implement-canfulfillintentrequest-for-name-free-interaction.html
  * https://developer.amazon.com/docs/custom-skills/understand-name-free-interaction-for-custom-skills.html
- deploy lambda as API endpoint https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html#api-gateway-proxy-integration-create-lambda-backend
