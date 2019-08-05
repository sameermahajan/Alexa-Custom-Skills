import requests

url = 'https://api.amazonalexa.com/v1/proactiveEvents/stages/development'
headers = {'Content-Type':'application/json', 'Authorization' : '<code got in earlier step>'}
body = """{
  "timestamp": "2019-08-05T12:11:30.00Z",
  "referenceId": "b5337856-1867-40dc-9d66-67bef92080f3",
  "expiryTime": "2019-08-05T20:11:30.00Z",
  "relevantAudience": {
    "type": "Multicast",
    "payload": {}
  },
  "event": {
    "name": "AMAZON.MessageAlert.Activated",
    "payload": {
      "state": {
        "status": "UNREAD",
        "freshness": "NEW"
      },
      "messageGroup": {
        "creator": {
          "name": "Sinus Congestion"
        },
        "count": 5,
        "urgency": "URGENT"
      }
    }
  }
}"""
ret = requests.post(url, headers = headers, json = body)
print (("ret = {} ret status_code = {} ret.text = {}").format(ret, ret.status_code, ret.text))
