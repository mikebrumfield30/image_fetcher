import json
import boto3
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs

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
        "Authorization": f"Client-ID {auth['access_key']}"
    }
    endpoint = f"{base_url}/search/photos"
    params = {
        "query": query
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()


def parse_width_from_url(url):
    parsed = urlparse.urlparse(url)
    width = int(parse_qs(parsed.query)['w'][0])
    return width


def format_photos(photo_results):
    formatted_list = []
    hits = photo_results['results']
    first_six = hits[0:num_images_to_get]
    for img in first_six:
        formatted_list.append({
            'id': f"unsplash-{img['id']}",
            'url': img['urls']['small'],
            'height': 'unknown',
            'width': int(parse_width_from_url(img['urls']['small'])),
            'author': img['user']['id']
        })
    return formatted_list


def perform_batch_fetch(term):
    photos = get_photos(term)
    formatted_photos = format_photos(photos)
    return formatted_photos
