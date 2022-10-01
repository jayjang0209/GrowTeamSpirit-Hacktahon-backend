import json
import boto3
import os
import traceback
from api import utils
from api.user.handlers import get_user_data, update_user_data


DYNAMODB = boto3.resource('dynamodb')
TABLE_NAME_USER = os.getenv('USER_TABLE')
USER_TABLE = DYNAMODB.Table(TABLE_NAME_USER)

def lambda_handler(event, context):
    resource = event['resource']
    method = event['httpMethod']
    
    res = utils.build_response(200, event)

    try:
        if method == "GET":
            if '/user/{user_id}' in resource:
                res = get_user_data(event, USER_TABLE)
                
        if method == 'PATCH':
            if '/user/{user_id}' in resource:
                res = update_user_data(event, USER_TABLE)
    
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
