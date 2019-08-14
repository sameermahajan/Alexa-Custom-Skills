import json
import time

def lambda_handler(event, context):
    print (time.time())
    print ("event = " + str(event))
    time.sleep(20)
    print (time.time())

    return {
        'statusCode': 200,
        'body': json.dumps('successfully waited 10 seconds for ' + str(event['queryStringParameters']['name']))
    }
