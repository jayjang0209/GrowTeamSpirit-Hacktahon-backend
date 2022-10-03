import json
from api import utils
from boto3.dynamodb.conditions import Key, Attr
import boto3
from botocore.exceptions import ClientError

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


def send_invitation(event, table):

    user_email = event['pathParameters']['user_email']
    event_id = event['pathParameters']['event_id']

    # This address must be verified with Amazon SES.
    SENDER = 'zhangqiangtianchen@gmail.com'
  
    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = user_email
    
    res = table.get_item(
        Key={'id': event_id}
    )
    event = res['Item']
    
    event_category = event['interest']
    date = event['date']
    city = event['city']
    place = event['place']
    time = event['time']



    # The subject line for the email.
    SUBJECT = f"invitation for {event_category} event on {date} in {city}"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
        <h1>Biweekly Event invitation !!</h1>
        <p>Hi, this is a invitation for {event_category} event on {date} in {city}.</p>
        
        <h2>Event Details</h2>
        <p>Date: {date}</p>
        <p>Time: {time}</p>
        <p>Place: {place}</p>
        <p>Category: {event_category}</p>
        <p>City: {city}</p>

        <p>
            <a href='https://4fhkr2hwj3.execute-api.us-west-2.amazonaws.com/prod/event/accept-event/{user_email}/{event_id}'>
                Accept the invitation
            </a>
        </p>
        
        <p>Thank you</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create SES client (edited)
    ses = boto3.client('ses')
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    return utils.build_response(200, 'email sent successfully')