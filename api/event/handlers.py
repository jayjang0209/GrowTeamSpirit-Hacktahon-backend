import json
from api import utils
from boto3.dynamodb.conditions import Key, Attr

# accept_event, cancel_event, get_participants

def accept_event(event, table):
    user_email = event['pathParameters']['user_email']
    event_id = event['pathParameters']['event_id']
    res = table.get_item(
        Key={
            'id': event_id
        }
    )
    event = res['Item']
    event['user_emails'].append(user_email)
    table.put_item(
        Item=event
    )
    return utils.build_response(200, 'event accepted')

def cancel_event(event, table):
    event_id = event['pathParameters']['event_id']
    user_email = event['pathParameters']['user_email']

    res = table.get_item(
        Key={
            'id': event_id
        }
    )
    event = res['Item']
    event['user_emails'].remove(user_email)
    table.put_item(
        Item=event
    )
    return utils.build_response(200, 'event cancelled')

def get_participants(event, table):
    event_id = event['pathParameters']['event_id']
    res = table.get_item(
        Key={
            'id': event_id
        }
    )
    event = res['Item']
    return utils.build_response(200, event['user_emails'])

def get_event(event, table):
    event_id = event['pathParameters']['event_id']
    res = table.get_item(
        Key={
            'id': event_id
        }
    )
    event = res['Item']
    return utils.build_response(200, event)

def get_my_events(event, table):
    user_email = event['pathParameters']['user_email']
    res = table.scan(
        FilterExpression=Attr('user_emails').contains(user_email)
    )
    events = res['Items']
    return utils.build_response(200, events)