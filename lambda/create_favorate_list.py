import json
import boto3
import uuid

def lambda_handler(event, context):
    
    # TODO retrive access_token from event
    clientId = "28rtt451qusispi2q63ecb880h"
    # access_token = event['multiValueQueryStringParameters']['access_token'][0]
    access_token = 'eyJraWQiOiJ4UXF4Z2N6T1lcLzhsTlwvZjZ5aGJFNGNyRURicVZVam1KVTdcL1lnd1ZKakxFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlNjNkNDM4ZC0xMGJjLTQ5YTMtODcxMi1mODlmZTRlODUwMWUiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TVG1ha0xOWXkiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIyOHJ0dDQ1MXF1c2lzcGkycTYzZWNiODgwaCIsIm9yaWdpbl9qdGkiOiI3NzU2YjMxYy00MmFhLTQxMWEtYWE5NS00NjZjNGRjZGMwYjIiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjUxOTU5Mzk3LCJleHAiOjE2NTE5NjI5OTcsImlhdCI6MTY1MTk1OTM5NywianRpIjoiNzI1ZmI1YTktZmI4Ni00MTA3LWIwODAtNmExNmQxMWI3MTA3IiwidXNlcm5hbWUiOiJlNjNkNDM4ZC0xMGJjLTQ5YTMtODcxMi1mODlmZTRlODUwMWUifQ.et0dUapi637YTRlRPUWUi0lC56UK-KgNF_4jgIcjKlcG4AVv2Cd9gyWcDjMLXcQi1WJudvDik_fOfoEGmk4nGt4h7Zyvk4nHooKZ2wcAkA8D0j47WRC7sJo2AQchAXgGAPHkTjm_mnXcgjPMXsMFAAvWkbVIm8P3gRdRD3eIAplaidMMDCXdcxGLqTxSV6DTwUsSPjvZqGInJQNvk3fOLgFr-HtWKHjVB7VwOVn79w1Ef9LJQUCbDhrjBZ7N41CTtC7HsOLKIbLsfRWsEQmot7wJhmnaEdLh-vPGsXB_OFDKqJ86RZYmXK_WAMUhKGlZP_ntxkiHR-UCIF55aCMyYA'
    
    data = dict()
    data['fid'] = str(uuid.uuid4())
    data['rid_list'] = []
    data['uid_list'] = [get_uid(clientId, access_token)]
    
    table_name = 'favorate-list'
    insert_data([data], table_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Create favorate list success!'),
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
    

def insert_data(data_list, table, db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    # overwrite if the same index is provided
    for data in data_list:
        response = table.put_item(Item=data)

    print('@insert_data: response', response)
    
    
    # return response
