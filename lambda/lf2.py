import json

import boto3
import requests
from botocore.exceptions import ClientError
from decimal import Decimal


def get_query_json(rating_gte, price_levels, cuisine_type):
  must_match = [{
    "bool": {
      "should": [{
        "match_phrase": {
          "price.keyword": price_level
        }
      } for price_level in price_levels],
      "minimum_should_match": 1
    }
  }, {
    "range": {
      "rating": {
        "gte": rating_gte
      }
    }
  }]
  if cuisine_type:
    must_match.append(
      {"bool": {
        "should": [{
          "match_phrase": {
            "categories.keyword": cuisine_type
          }
        }],
        "minimum_should_match": 1
      }})

  return {"query": {"bool": {"must": must_match}}}


def lambda_handler(event, context):
  print(event)
  queryParams = event['queryStringParameters']
  cuisine_type = queryParams.get('cuisine', None)
  price_level = queryParams.get('price_level', "$$$$")
  rating_gte = queryParams.get('rating', 0)

  headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
  elastic_url = 'https://search-newomegameal-gtoulkq2wurnbuviwepd7ycria.us-east-1.es.amazonaws.com/restaurants/_search'

  # rating_gte, price_levels, cuisine_type
  query = get_query_json(
    rating_gte=rating_gte,
    price_levels=["$" * i for i in range(1,
                                         len(price_level) + 1)],  # need pre-processing
    cuisine_type=cuisine_type)

  response = requests.get(elastic_url,
                          data=json.dumps(query),
                          auth=('master', 'Master-6998'),
                          verify=False,
                          headers=headers)
  data = json.loads(response.text)
  rids = get_rid(data)
  restaurants = []
  for rid in rids:
    restaurant = lookup_data({"rid": rid})
    for key in restaurant:
      if isinstance(restaurant[key], Decimal):
        restaurant[key] = float(restaurant[key])
    restaurants.append(restaurant)

  return {
    'statusCode': 200,
    'body': json.dumps(restaurants),
    'headers': {
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,OPTIONS',
    },
  }


def get_rid(raw):
  print(raw)
  rids = []
  for i in raw['hits']['hits']:
    rids.append(i['_source']['rid'])
  return rids


def lookup_data(key, db=None, table='restaurants'):
  if not db:
    db = boto3.resource('dynamodb')
  table = db.Table(table)
  try:
    response = table.get_item(Key=key)
  except ClientError as e:
    print('Error', e.response['Error']['Message'])
  else:
    print(response['Item'])
    return response['Item']
