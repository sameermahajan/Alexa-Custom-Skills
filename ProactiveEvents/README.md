# Proactive Events

You can send async notifications / events to alexa.

You can read more details at: https://developer.amazon.com/docs/smapi/proactive-events-api.html

These events can currently follow only predefined schemas as outlined in: https://developer.amazon.com/docs/smapi/schemas-for-proactive-events.html#event-catalog

For detailed steps you can follow the article at: https://medium.com/swlh/get-started-with-amazon-alexa-skills-proactive-events-api-5b082bcb282c

## Setup ASK CLI

```
sudo apt-get install nodejs
sudo apt install npm
sudo npm install -g ask-cli
ask init
```

## Add events to skill

Get the skill manifest as a json file

```
ask api get-skill -s skill_id > skill.json
```

Edit the jason to add something like

```
    "events": {
      "publications": [
        {
          "eventName": "AMAZON.MessageAlert.Activated"
        },
        {
          "eventName": "AMAZON.SportsEvent.Updated"
        }
      ],
      "endpoint": {
        "uri": "arn:aws:lambda:us-east-1:<id>:function:sameer_alexa_test"
      }
    },
```

to the "manifest" section.

Update the skill with the corrected manifest

```
ask api update-skill -s skill_id -f skill.json
```

Check skill status — if it is updated correct, status will contain SUCCESS

```
ask api get-skill-status -s skill_id
```

## Skill Client Id and Client Secret

Developer Console for the Alexa Skill should contain now Client Id and Client Secret for this skill. Enable this skill on your device and allow notifications.

## Request a bearer token

Execute request_bearer_token.py given in this repo to get the bearer token.

## Send proactive notification

Execute send_aync_notification.py given in this repo to send an async / proactive notification.

At this time you can check your device and read the notification.

## Event audience options

You can use Unicast type to send notification to a specific user id.

To track user-ids — subscribe on an event, notifying that a user turned on/off proactive notifications. To make the skill’s Lambda function receive this event — add following subscription section to the Alexa skill manifest (to the “events” property) and update the manifest with the ASK-CLI

```
"subscriptions": [
  {
    "eventName": "SKILL_PROACTIVE_SUBSCRIPTION_CHANGED"
  }
]
```

Your skill's manifest (can be checked by doing ask api get-skill) will now look something like

```
{
  "manifest": {
    "apis": {
      "custom": {
        "endpoint": {
          "uri": "arn:aws:lambda:us-east-1:<id>:function:sameer_alexa_test"
        },
        "interfaces": []
      }
    },
    "events": {
      "publications": [
        {
          "eventName": "AMAZON.MessageAlert.Activated"
        },
        {
          "eventName": "AMAZON.SportsEvent.Updated"
        }
      ],
      "endpoint": {
        "uri": "arn:aws:lambda:us-east-1:<id:function:sameer_alexa_test"
      },
      "subscriptions": [
        {
          "eventName": "SKILL_PROACTIVE_SUBSCRIPTION_CHANGED"
        }
      ]
    },
    "manifestVersion": "1.0",
    "permissions": [
      {
       ....
```

You can then handle this event in your lambda e.g. by cataloging this user id etc. The user id should appear in

```
event.context.System.user.userId
```

and is something like

```
amzn1.ask.account.AH...
```
