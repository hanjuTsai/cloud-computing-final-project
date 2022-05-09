import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    
    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = event['headers']['access_token']
    uid = get_uid(clientId, access_token)
    
    table_name = 'follow'
    
    follow_uid_list = get_follow_uid_list(uid, table_name)
    
    table_name = 'favorite-list'
    
    follow_favorite_list = dict()
    
    for followed_uid in follow_uid_list:
        
        #check the user have favorite list or not, is not create it
        create_dynamalDB(followed_uid, table_name)
        favorite_list = get_favorite_list(followed_uid, table_name)
        detail_list = ridList_to_detailList(favorite_list['rid_list'])
        follow_favorite_list[followed_uid] = detail_list
    
        print(f"{uid}'s favorite list (rid_list):", favorite_list['rid_list'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(follow_favorite_list),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access_token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS',
        },
    }

def ridList_to_detailList(rid_list):
    
    rid_list_with_detail = []
    for rid in rid_list:
      restaurant = lookup_data({"rid": rid})
      for key in restaurant:
        if isinstance(restaurant[key], Decimal):
          restaurant[key] = float(restaurant[key])
      rid_list_with_detail.append(restaurant)
    
    return rid_list_with_detail
    

def get_uid(clientId ,access_token):
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.get_user(AccessToken=access_token)
    
    for attr in response['UserAttributes']:
        if attr['Name'] == 'email':
            id = attr['Value']
    
    return id
    
    
def get_favorite_list(uid, table, db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    data = table.get_item(Key = {'uid':uid})
    
    if 'Item' not in data:
        return []

    return data['Item']

    
def lookup_data(key, db=None, table='restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        # print(response['Item'])
        return response['Item']


def create_dynamalDB(uid, table, db=None):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    response = table.get_item(Key = {'uid':uid})
    
    if 'Item' not in response.keys():
        
        data = dict()
        data['uid'] = uid
        data['rid_list'] = []
        response = table.put_item(Item=data)
        
        print(f"{uid}'s favorite list has created")
        
        
def get_follow_uid_list(uid, table, db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    response = table.get_item(Key = {'uid':uid})
    
    if 'Item' not in response.keys():
        
        data = dict()
        data['uid'] = uid
        data['following_uid_list'] = []
        response = table.put_item(Item=data)
        
        print(f"{uid}'s favorite list has created")
        
        response = table.get_item(Key = {'uid':uid})
        
    return response['Item']['following_uid_list']
