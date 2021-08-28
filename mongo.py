from app_config import mongo_url
from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient(mongo_url)
raw_db = client['raw']

try:
    client.server_info()
    print(f'connected to {mongo_url}')
except Exception:
    print("Unable to connect to the server.")


def insert_imgs_for_review(imgs):
    img_col = raw_db['images_for_review']

    accepted_imgs = []

    for _ in range(0, len(imgs)):
        existing = img_col.find_one({
            'id': imgs[_]['id']
         })
        if existing is None:
            accepted_imgs.append(imgs[_])

    x = img_col.insert_many(imgs)
    print(x.inserted_ids, x.acknowledged)


# example
if __name__ == "__main__":
    fake_imgs = [
        {
            'id': 'fake',
            'width': 240,
            'height': 500,
            'url': 'todo2.com'
        },
        {
            'id': 'fake',
            'width': 240,
            'height': 500,
            'url': 'todo1.com'
        }
    ]
    fake_img = {
            'id': 'fake',
            'width': 240,
            'height': 500,
            'url': 'todo1.com'
        }
    insert_imgs_for_review(fake_imgs)