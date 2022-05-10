import json
import numpy as np
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from PIL import Image
import requests
from scipy.special import softmax



def lambda_handler(event, context):
    # TODO implement
    
    
    rid = event['queryStringParameters']['rid']
    score = sagemaker_inference_score(rid,True)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(score),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS',
        },
    }

def sagemaker_inference_score(rid, resnet = False):
    
    score = 0
    
    restaurant = lookup_data({"rid": rid})
    
    if resnet:
        
        url = restaurant['image_url']
        im = Image.open(requests.get(url, stream=True).raw).resize((224,224))
        im = np.array(im).astype(np.float32)
        im = np.moveaxis(im, 2, 0)
        im = np.expand_dims(im, axis=0)
        runtime= boto3.client('runtime.sagemaker')
        response = runtime.invoke_endpoint(EndpointName="pytorch-training-2022-05-10-21-14-40-252",
                                      ContentType='application/json',
                                      Body=json.dumps(im.tolist()))
        
        response = json.loads(response["Body"].read().decode("utf-8"))
        
        proba = softmax(response[0])
        
        
        score = np.max(proba)
        
        if int(restaurant['label']) == 0:
            score = 1- np.max(proba)
            
        print(proba)
                                      
    else:
        print(restaurant)
    
        score = np.random.uniform(0,46)
        if int(restaurant['label']) == 1:
            score = np.random.uniform(52,96)
        
    return score*100
    

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

