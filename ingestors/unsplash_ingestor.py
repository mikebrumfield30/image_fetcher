import json
import boto3
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import random

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


def format_photos(photo_results, plant_name):
    formatted_list = []
    hits = photo_results['results']
    if len(hits) == 0:
        return []
    print(f'length of parsed photos: {len(hits)}')
    # need to first check that the length of fetched images is less than the amount requested
    if len(hits) > num_images_to_get:
        lower = random.randint(0, len(hits) - (1 + num_images_to_get))
    else:
        lower = random.randint(0, len(hits))
    higher = lower + num_images_to_get
    selected_imgs = hits[lower:higher]
    for img in selected_imgs:
        formatted_list.append({
            'id': f"unsplash-{img['id']}",
            'url': img['urls']['small'],
            'height': 'unknown',
            'width': int(parse_width_from_url(img['urls']['small'])),
            'author': img['user']['id'],
            'plantName': plant_name
        })
    return formatted_list


def perform_batch_fetch(term, plant_name):
    photos = get_photos(term)
    formatted_photos = format_photos(photos, plant_name)
    return formatted_photos
