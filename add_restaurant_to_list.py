import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    
    # TODO retrive access_token from event
    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = event['headers']['access_token']
    
    rid = event['queryStringParameters']['rid']
    uid = get_uid(clientId, access_token)
    
    table_name = 'favorite-list'
    
    #check did the user have favorite list, is not create it
    create_dynamalDB(uid, table_name)
    update_dynomalDB(uid, rid, table_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }


def get_uid(clientId ,access_token):
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.get_user(AccessToken=access_token)
    
    for attr in response['UserAttributes']:
        if attr['Name'] == 'email':
            id = attr['Value']
    
    return id
    
    
def update_dynomalDB(uid, rid, table, db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    response = table.get_item(Key = {'uid':uid})
    
    if rid not in response['Item']['rid_list']:
    
        response = table.update_item(
            Key = {'uid':uid},
            UpdateExpression="SET rid_list = list_append(rid_list, :i)",
            ExpressionAttributeValues={
                ':i': [rid],
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"{rid} has been added to {uid}'s favorite list")
    else:
        print(f"{rid} already in {uid}'s favorite list")

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
    
