import urllib3
import json
import os

http = urllib3.PoolManager()
url = os.environ.get("WEBHOOK_URL", "")

def handler(event, context):

    if not url:
        print("No webhook URL provided.")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Webhook URL not configured"})
        }

    msg = {
        "channel": "#all-aws-events",
        "text": event['Records'][0]['Sns']['Message'],
    }
    
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print({
        "message": event['Records'][0]['Sns']['Message'], 
        "status_code": resp.status, 
        "response": resp.data
    })