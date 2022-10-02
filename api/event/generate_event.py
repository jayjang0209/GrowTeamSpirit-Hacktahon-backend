import json
import boto3
import os
import traceback
from boto3.dynamodb.conditions import Key, Attr
import datetime
import random

DYNAMODB = boto3.resource('dynamodb')
TABLE_NAME_USER = os.getenv('USER_TABLE')
TABLE_NAME_EVENT = os.getenv('EVENT_TABLE')
USER_TABLE = DYNAMODB.Table(TABLE_NAME_USER)
EVENT_TABLE = DYNAMODB.Table(TABLE_NAME_EVENT)
INTEREST_CATEGORY = ['sports', 'outings']
MOCK_EVENT_TIME = ["7:00 PM", "7:15 PM", "7:30 PM", "7:45 PM", "8:00 PM"]
MOCK_EVENT_PLACE = ['1111 Main street', '2222 Wall street', '3333 5th street', '4444 6th street', '5555 7th street', '6666 8th street', '7777 9th street', '8888 10th street', '9999 11th street', '1010 12th street', '1111 13th street', '1212 14th street', '1313 15th street', '1414 16th street', '1515 17th street', '1616 18th street', '1717 19th street', '1818 20th street', '1919 21st street', '2020 22nd street', '2121 23rd street', '2222 24th street', '2323 25th street', '2424 26th street', '2525 27th street', '2626 28th street', '2727 29th street', '2828 30th street', '2929 31st street', '3030 32nd street', '3131 33rd street', '3232 34th street', '3333 35th street', '3434 36th street', '3535 37th street', '3636 38th street', '3737 39th street', '3838 40th street', '3939 41st street', '4040 42nd street', '4141 43rd street', '4242 44th street', '4343 45th street', '4444 46th street', '4545 47th street', '4646 48th street', '4747 49th street', '4848 50th street', '4949 51st street', '5050 52nd street', '5151 53rd street', '5252 54th street', '5353 55th street', '5454 56th street', '5555 57th street', '5656 58th street', '5757 59th street', '5858 60th street', '5959 61st street', '6060 62nd street', '6161 63rd street', '6262 64th street', '6363 65th street', '6464 66th street']


def lambda_handler(event, context):
    all_interests = get_all_interest(USER_TABLE)
    print(all_interests)
    all_cities = get_all_cities(USER_TABLE)
    print(all_cities)

    for city in all_cities:
        for interest in all_interests:
            filtered_users =  [user["email"] for user in get_filtered_users(USER_TABLE, interest, city)]
            generate_event(EVENT_TABLE, interest, city, filtered_users)


def get_all_interest(table):

    unique_interest = []
    
    for category in INTEREST_CATEGORY:
        res = table.scan(
            AttributesToGet = [category]
        )

        for item in res['Items']:
            if category in item.keys():
                for interest in item[category]:
                    if interest not in unique_interest:
                        unique_interest.append(interest)

    return unique_interest

def get_all_cities(table):
    unique_cities = []

    res = table.scan(
        AttributesToGet = ['city']
    )

    for city in res['Items']:
        if 'city' in city.keys() and city['city'] not in unique_cities:
                unique_cities.append(city['city'])

    return unique_cities

def get_filtered_users(table, interest, city):
    res = table.scan(
        FilterExpression=Attr('city').eq(city) and Attr('sports').contains(interest)
    )
    
    if len(res['Items']) == 0:
        res = table.scan(
            FilterExpression=Attr('city').eq(city) and Attr('outings').contains(interest)
    )

    return res['Items']

def generate_event(table, interest, city, user_emails):
    date = get_two_weeks_date()
    event = {
        'id': generate_id(city, interest, date),
        'interest': interest,
        'date': date,
        'user_emails': [],
        'time': pick_random_item(MOCK_EVENT_TIME),
        'city': city,
        'place': pick_random_item(MOCK_EVENT_PLACE)
    }
    table.put_item(Item=event)

def get_two_weeks_date():
    today = datetime.datetime.today()
    two_weeks = today + datetime.timedelta(days=14)
    return two_weeks.strftime('%Y-%m-%d')

def pick_random_item(list):
    return list[random.randint(0, len(list) - 1)]

def generate_id(city, interest, date):
    return str(city) + "-"+ str(interest) + "-" +str(date)