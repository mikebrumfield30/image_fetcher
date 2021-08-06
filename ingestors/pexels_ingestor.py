import json
import boto3
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os

num_images_to_get = 6
base_url = "https://api.pexels.com/v1"


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
        if k['name'].lower() == 'pexels':
            return k['key']


def get_photos(query):
    auth = get_auth()
    headers = {
        "Authorization": auth['api_key']
    }
    endpoint = f"{base_url}/search"
    params = {
        "query": query
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()


def parse_width_and_height_from_url(url):
    parsed = urlparse.urlparse(url)
    height = int(parse_qs(parsed.query)['h'][0])
    width = int(parse_qs(parsed.query)['w'][0])
    return width, height


def format_photos(photos):
    formatted_photos = []
    parsed_photos = photos['photos']
    first_six = parsed_photos[0:num_images_to_get]
    for img in first_six:
        width, height = parse_width_and_height_from_url(img['src']['large'])
        formatted_photos.append({
            'id': f"pexels-{img['id']}",
            'url': img['src']['large'],
            'height': height,
            'width': width,
            'author': img['photographer']
        })
    return formatted_photos


def perform_batch_fetch(term):
    photos = get_photos(term)
    formatted_photos = format_photos(photos)
    return formatted_photos
