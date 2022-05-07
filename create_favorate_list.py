import json
import boto3
import uuid

def lambda_handler(event, context):
    
    # TODO retrive access_token from event
    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = 'eyJraWQiOiJ4UXF4Z2N6T1lcLzhsTlwvZjZ5aGJFNGNyRURicVZVam1KVTdcL1lnd1ZKakxFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzODMyNDRiOC0yYzYxLTQ4ODctYTM1OC1mOWVkZWI2ZDNjMDMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TVG1ha0xOWXkiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIyOHJ0dDQ1MXF1c2lzcGkycTYzZWNiODgwaCIsIm9yaWdpbl9qdGkiOiJiOTU4ZGQzZS01Mzc1LTQ3N2ItYTFlMS03YTViMTQzZDUyMGMiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjUxOTQzODM1LCJleHAiOjE2NTE5NDc0MzUsImlhdCI6MTY1MTk0MzgzNSwianRpIjoiODY0OWM5ZGEtMmIzNC00NzIzLThlNzItYzVjZTUzYTlmYTY1IiwidXNlcm5hbWUiOiIzODMyNDRiOC0yYzYxLTQ4ODctYTM1OC1mOWVkZWI2ZDNjMDMifQ.XV9gc_D2WTub7mOl6f2LgEyAYglhQH6hxuz3UDsMSs2oniMFohIfMw0OZSbMQ7yjE2v0S5F20b35LF1HBWjm-jq6jh5v9SevSy7QyL4raKqGMx7vZdJ0XplpD5g8C5uVfOEmpMWafcbrUI_kg3v4QoFuASsjznkiRTs1x0ASuWBhgb34Oj6MAF43_gLp4HfEhMWOa_O4ajFq1Dw7cDekQicv4Yabh25g1garpNTyqehhqGym_TOFNpfqvS1TafJg3FPh9L441BSriLkbosp9rHzX0sFPMr5rGkvlf2w4FOeKu9zMDMaJqIiavqLqHJohXREUkNNyADSxvyR6o39_-w'
    
    data = dict()
    data['fid'] = str(uuid.uuid4())
    data['rid_list'] = []
    data['uid_list'] = [get_uid(clientId, access_token)]
    
    table_name = 'favorate-list'
    insert_data([data], table_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Create favorate list success!')
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


