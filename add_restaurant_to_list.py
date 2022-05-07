import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    
    # TODO retrive access_token from event
    clientId = "28rtt451qusispi2q63ecb880h"
    access_token = 'eyJraWQiOiJ4UXF4Z2N6T1lcLzhsTlwvZjZ5aGJFNGNyRURicVZVam1KVTdcL1lnd1ZKakxFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlNjNkNDM4ZC0xMGJjLTQ5YTMtODcxMi1mODlmZTRlODUwMWUiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TVG1ha0xOWXkiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIyOHJ0dDQ1MXF1c2lzcGkycTYzZWNiODgwaCIsIm9yaWdpbl9qdGkiOiI0ZjViY2M5OC1hODg4LTRlZGYtYWQ2OC1hOGU0Y2YzZjE2ODkiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjUxOTQ4Mjk4LCJleHAiOjE2NTE5NTE4OTgsImlhdCI6MTY1MTk0ODI5OCwianRpIjoiNWJhNWI4ZDQtMGE5NS00NDlhLWIwMjgtYTdkNzhhNTNlYTQyIiwidXNlcm5hbWUiOiJlNjNkNDM4ZC0xMGJjLTQ5YTMtODcxMi1mODlmZTRlODUwMWUifQ.cCmbuVeoVyUQm2erLaRua73jWFCndvcKYdphbruxS9EEYyeInwHacfePB9giXGRjFpBej0z0JQD9Dr_eJvuFfiWprWqtqWGPGH3n43-kkMJQYDjGsILFTgDDtJ_SYSj08IkBzZGUCi2Bf6ruGEVTck7O3V_uLe4zSRe_LM-TIkO1w7QP3XWq2jQ-z6rpHxRkwhatIUOq-EzMv4Iyb01Zl_qvOQktMGksTG-GA1W-3c6s9j5to_A0-lOzSZN5z1ks6P0SawTbvzB80fllxElCOA8j2eGlDwvLqjvjxLeCanGabkO_Rk1vv__Y1q3ckuImAPQ5wqUOKgNFlkiOtAnBhA'
    
    # TODO retrive fid, rid from event
    fid = '5aca4734-5127-4922-8591-63c077493cdc'
    rid = 'HSQodPxknZmHsiKQOqtQ5A'
    uid = get_uid(clientId, access_token)
    
    table_name = 'favorate-list'
    favorate_list_list = update_dynomalDB(fid, rid, table_name)
    
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
    
    
def update_dynomalDB(fid, rid, table, db=None):
    
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    
    response = table.update_item(
        Key = {'fid':fid},
        UpdateExpression="SET rid_list = list_append(rid_list, :i)",
        ExpressionAttributeValues={
            ':i': [rid],
        },
        ReturnValues="UPDATED_NEW"
    )

