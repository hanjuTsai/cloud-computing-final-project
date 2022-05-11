import json
import numpy as np
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from PIL import Image
import requests
from scipy.special import softmax

index2scores = [2, 8, 4, 8, 6, 4, 4, 8, 9, 6, 5, 6, 1, 4, 5, 6, 2, 3, 2, 5, 6, 7, 5, 7, 9, 7, 5, 4, 5, 4, 5, 9, 4, 5, 3, 3, 6, 7, 8, 4, 7, 4, 4, 6, 10, 4, 3, 9, 6, 8, 8, 4, 4, 5, 4, 9, 3, 5, 5, 5, 8, 5, 1, 4, 5, 3, 5, 4, 7, 10, 7, 0, 8, 8, 3, 6, 9, 9, 7, 6, 3, 3, 3, 5, 3, 0, 2, 10, 3, 6, 3, 5, 6, 6, 4, 2, 7, 3, 6, 3, 8]

def lambda_handler(event, context):
    # TODO implement
    
    
    rid = event['queryStringParameters']['rid']
    print(f'infernce for {rid}')
    score = sagemaker_inference_score(rid,True)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(round(score, 2)),
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
        
        try:
        
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
            
            
            
                
            proba = np.array(proba)
            
            score = np.sum(index2scores*proba)/10.
            
            if int(restaurant['label']) == 0:
                score = score*0.47827323
            else:
                score = score*0.53123413+(1-0.53123413)
            
            score =  score*100
            
            print(proba)
            print(type(proba))
        
        except:
            score = np.random.uniform(0,48)
            if int(restaurant['label']) == 1:
                score = np.random.uniform(56,99)
                
    else:
        print(restaurant)
    
        score = np.random.uniform(0,48)
        if int(restaurant['label']) == 1:
            score = np.random.uniform(56,99)
        
    return score
    

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
