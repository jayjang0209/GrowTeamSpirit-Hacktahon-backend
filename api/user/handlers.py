import json
from api import utils
from boto3.dynamodb.conditions import Key, Attr

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


def get_all_list_of_attribute(event, table):
    category = event['pathParameters']['category']

    res = table.scan(
        AttributesToGet = [category]
    )
    
    unique_attribute = []

    for item in res['Items']:
        if category in item.keys():
            if item[category] not in unique_attribute:
                unique_attribute.append(item[category])

    # unique_interest = []
    # for item in res['Items']:
    #     if category in item.keys():
    #         for interest in item[category]:
    #             if interest not in unique_interest:
    #                 unique_interest.append(interest)
    return utils.build_response(200, unique_attribute)


def get_all_list_of_interest(event, table):
    """
    Get all list of each interest.

    :param event: JSON formatted data triggered from an HTTP call via API gateway
    :param table: target table
    :return: response containing status code, headers, and body
    """
    category = event['pathParameters']['category']

    res = table.scan(
        AttributesToGet = [category]
    )

    unique_interest = []
    for item in res['Items']:
        if category in item.keys():
            for interest in item[category]:
                if interest not in unique_interest:
                    unique_interest.append(interest)
    return utils.build_response(200, unique_interest)


def get_filtered_user(event, table):
    """
    Get filtered user.

    :param event: JSON formatted data triggered from an HTTP call via API gateway
    :param table: target table
    :return: response containing status code, headers, and body
    """
    city = event['pathParameters']['city']
    interest = event['pathParameters']['interest']
    print(city)
    print(interest)

    res = table.scan(
        FilterExpression=Attr('city').eq(city) and Attr('sports').contains(interest)
    )
    
    if len(res['Items']) == 0:
        res = table.scan(
            FilterExpression=Attr('city').eq(city) and Attr('outings').contains(interest)
    )


    return utils.build_response(200, res['Items'])
