import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    

    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = event['headers']['access_token']

    rid = event['queryStringParameters']['rid']
    uid = get_uid(clientId, access_token)
    
    status = remove_rid_from_list(uid, rid)
    
    return {
        'statusCode': 200,
        'body': json.dumps('success'),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,access_token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS,DELETE',
        },
    }



def get_uid(clientId ,access_token):
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.get_user(AccessToken=access_token)
    
    for attr in response['UserAttributes']:
        if attr['Name'] == 'email':
            id = attr['Value']
    
    return id
    
    
def remove_rid_from_list(uid, rid, tablename= "favorite-list", db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(tablename)
    
    data =  table.get_item(Key = {'uid':uid})["Item"]
    
    try:
        removed_index = data['rid_list'].index(rid)
    
        response = table.update_item(
            Key = {'uid':uid},
            UpdateExpression=f"REMOVE rid_list[{removed_index}]",
            ReturnValues="UPDATED_NEW"
        )
        
        print(f"remove {rid} from {uid}'s favorite list")
        
    except:
        print(f"{rid} do not exist in {uid}'s favorite list or {uid} has no favorit list")


