import json
import boto3
import requests
import os

num_images_to_get = 6
base_url = "https://api.unsplash.com"


def get_param(param_name):
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name=param_name
    )
    return json.loads(response['Parameter']['Value'])


def get_auth():
    # param = os.getenv("API_KEY")
    full_auth = get_param("/synthesis/api/image-fetcher")
    for k in full_auth['keys']:
        if k['name'].lower() == 'unsplash':
            return k['key']


def get_photos(query):
    auth = get_auth()
    headers = {
        "Client-ID": auth['access_key']
    }
    endpoint = f"{base_url}/search/photos"
    params = {
        "query": query
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response
