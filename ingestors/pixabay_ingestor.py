import json
import boto3
import requests
import os

num_images_to_get = 6
base_url = "https://pixabay.com/api/"


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
        if k['name'].lower() == 'pixabay':
            return k['key']


def get_photos(query):
    auth = get_auth()
    endpoint = f"{base_url}"
    params = {
        "key": auth['api_key'],
        "q": query
    }
    response = requests.get(endpoint, params=params)
    return response.json()


def format_photos(photo_results):
    formatted_list = []
    hits = photo_results['hits']
    first_six = hits[0:num_images_to_get]
    for img in first_six:
        formatted_list.append({
            'id': f"pixabay-{img['id']}",
            'url': img['webformatURL'],
            'height': img['webformatHeight'],
            'width': img['webformatWidth'],
            'author': img['user']
        })
    return formatted_list


def perform_batch_fetch(term):
    photos = get_photos(term)
    formatted_photos = format_photos(photos)
    return formatted_photos
