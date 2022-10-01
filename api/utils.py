import json

def getResponseHeaders():
    return {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': getResponseHeaders(),
        'body': json.dumps(body)
    }