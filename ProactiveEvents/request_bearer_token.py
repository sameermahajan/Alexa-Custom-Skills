import requests
import ast

url = 'https://api.amazon.com/auth/o2/token'
headers = {'Content-Type':'application/x-www-form-urlencoded'}
body = {'grant_type' : 'client_credentials',
           'client_id' : '<your client id>',
           'client_secret' : '<your client secret>',
           'scope' : 'alexa::proactive_events'
           }
ret = requests.post(url, headers = headers, data = body)
print (ast.literal_eval(ret.text)["access_token"])
