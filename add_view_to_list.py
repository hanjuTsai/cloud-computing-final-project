import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

# update fid


def lambda_handler(event, context):

    # TODO retrive access_token from event
    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = event['headers']['access_token']
    uid = get_uid(clientId, access_token)
    
    table_name = 'follow'
    fid = event['queryStringParameters']['fid']
    
    msg = add_follower(uid, fid, table_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps(msg),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access_token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS',
        },
    }


def get_uid(clientId ,access_token):
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.get_user(AccessToken=access_token)
    
    for attr in response['UserAttributes']:
        if attr['Name'] == 'email':
            id = attr['Value']
    
    return id
    
def add_follower(uid, fid, table, db=None):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    try:
        data = table.get_item(Key = {'uid':uid})
        
        if fid not in data['Item']['following_uid_list']:

            response = table.update_item(
                Key = {'uid':uid},
                UpdateExpression="SET following_uid_list = list_append(following_uid_list, :i)",
                ExpressionAttributeValues={
                    ':i': [fid],
                },
                ReturnValues="UPDATED_NEW"
            )
            
            msg = f"added {fid} to the {uid}'s following_uid_list"
        else:
            msg = f" {fid} already in {uid}'s following_uid_list"
        
    except:
        data = dict()
        data['uid'] = uid
        data['following_uid_list'] = [fid]
        response = table.put_item(Item=data)
        
        msg = f"create favorate list for {uid} and added {fid} to the following_uid_list"
        
    print(msg)
    return msg
    
