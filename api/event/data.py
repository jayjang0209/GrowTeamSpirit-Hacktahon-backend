import json
import boto3
import os
import traceback
from api import utils
# from api.event.handlers import accept_event, cancel_event, get_participants
from api.event.handlers import accept_event, cancel_event, get_participants, get_event, get_my_events  


DYNAMODB = boto3.resource('dynamodb')
TABLE_NAME_USER = os.getenv('USER_TABLE')
TABLE_NAME_EVENT = os.getenv('EVENT_TABLE')
USER_TABLE = DYNAMODB.Table(TABLE_NAME_USER)
EVENT_TABLE = DYNAMODB.Table(TABLE_NAME_EVENT)

def lambda_handler(event, context):
    resource = event['resource']
    method = event['httpMethod']
    
    res = utils.build_response(200, event)

    try:
        if method == "GET":
            if '/event/get-participants/{event_id}}' in resource:
                res = get_participants(event, EVENT_TABLE)
            
            if '/event/get-event/{event_id}' in resource:
                res = get_event(event, EVENT_TABLE)

            if '/event/get-my-events/{user_email}' in resource:
                res = get_my_events(event, EVENT_TABLE)

            if '/event/accept-event/{user_email}/{event_id}' in resource:
                res = accept_event(event, EVENT_TABLE)

        if method == 'PATCH':
            if '/event/accept-event/{user_email}/{event_id}' in resource:
                res = accept_event(event, EVENT_TABLE)
            
            if '/event/cancel-event/{user_email}/{event_id}' in resource:
                res = cancel_event(event, EVENT_TABLE)

                
    
    except ValueError as e:
        traceback.print_exc()
        msg = {'errorMessage': "An error occurred parsing query string parameters. Please ensure they are the correct data type."}
        res = utils.build_response(400, msg)
    except Exception as e:
        traceback.print_exc()
        print('## EVENT DETAILS')
        print(event)
        print('## ERROR THROWN:')
        print(e)
        msg = {'errorMessage': "An error occurred. Please contact us so we may remedy the issue."}
        res = utils.build_response(500, msg)
    return res
