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


