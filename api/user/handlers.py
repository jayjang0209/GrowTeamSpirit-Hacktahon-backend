import json
from api import utils

def update_user_data(event, table):
    """
    Update the user's profile.

    :param event: JSON formatted data triggered from an HTTP call via API gateway
    :param table: target table
    :return: response containing status code, headers, and body
    """
    user_id = event['pathParameters']['user_id']
    item = json.loads(event['body'])

    table.update_item(
        Key={
            'id': user_id
        },
        ExpressionAttributeNames={
            '#gname': 'givenName',
            '#lname': 'familyName',
            '#email': 'email',
            '#country': 'country',
            '#province': 'province',
            '#city': 'city',
        },
        ExpressionAttributeValues={
            ':givenName': item['givenName'],
            ':familyName': item['familyName'],
            ':email': item['email'],
            ':country': item['country'],
            ':province': item['province'],
            ':city': item['city'],
        },
        UpdateExpression='SET #gname = :givenName, #lname = :familyName, #email = :email, #country = :country,'
                         '#province = :province, #city = :city',
        ReturnValues="UPDATED_NEW"
    )

    return utils.build_response(200, f"User Id: {user_id}'s data updated")


def update_user_interest(event, table):
    """
    Update the user's profile.

    :param event: JSON formatted data triggered from an HTTP call via API gateway
    :param table: target table
    :return: response containing status code, headers, and body
    """
    user_id = event['pathParameters']['user_id']
    item = json.loads(event['body'])

    table.update_item(
        Key={
            'id': user_id
        },
        ExpressionAttributeNames={
            '#sports': 'sports',
            '#pets': 'pets',
            '#outings': 'outings',
        },
        ExpressionAttributeValues={
            ':sports': item['sports'],
            ':pets': item['pets'],
            ':outings': item['outings'],
        },
        UpdateExpression='SET #sports = :sports, #pets = :pets, #outings = :outings',
        ReturnValues="UPDATED_NEW"
    )

    return utils.build_response(200, f"User Id: {user_id}'s data updated")

def get_user_data(event, table):
    """
    Get the user's profile.

    :param event: JSON formatted data triggered from an HTTP call via API gateway
    :param table: target table
    :return: response containing status code, headers, and body
    """
    user_id = event['pathParameters']['user_id']

    res = table.get_item(
        Key={'id': user_id}
    )
    return utils.build_response(200, res['Item'])
