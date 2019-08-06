import requests

url = 'https://api.amazonalexa.com/v1/proactiveEvents/stages/development'
headers = {'Content-Type':'application/json', 'Authorization' : '<code got in earlier step>'}
body = "{\r\n  \"timestamp\": \"2019-08-06T12:11:30.00Z\",\r\n  \"referenceId\": \"b5337856-1867-40dc-9d66-67bef92080f3\",\r\n  \"expiryTime\": \"2019-08-06T20:11:30.00Z\",\r\n  \"event\": {\r\n    \"name\": \"AMAZON.MessageAlert.Activated\",\r\n    \"payload\": {\r\n      \"state\": {\r\n        \"status\": \"UNREAD\",\r\n        \"freshness\": \"NEW\"\r\n      },\r\n      \"messageGroup\": {\r\n        \"creator\": {\r\n          \"name\": \"Sinus Congestion\"\r\n        },\r\n        \"count\": 5,\r\n        \"urgency\": \"URGENT\"\r\n      }\r\n    }\r\n  },\r\n  \"relevantAudience\": {\r\n    \"type\": \"Multicast\",\r\n    \"payload\": {}\r\n  }\r\n}"

response = requests.request("POST", url, data=body, headers=headers)

print (("response = {} response status_code = {} response.text = {}").format(response, response.status_code, response.text))
