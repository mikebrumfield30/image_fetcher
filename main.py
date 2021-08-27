import json
import boto3
import ingestors.unsplash_ingestor
import ingestors.pexels_ingestor
import ingestors.pixabay_ingestor
from datetime import datetime
from mongo import insert_imgs_for_review
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to get some free images from variety of API's and store "
                                                 "metadata in mongo")
    parser.add_argument('--query', type=str, nargs=1, required=True, help="Search term")

    args = parser.parse_args()
    query = args.query[0]
    query_no_space = query.strip().replace(' ', '_')
    pexels_imgs = ingestors.pexels_ingestor.perform_batch_fetch(query)
    pixabay_imgs = ingestors.pixabay_ingestor.perform_batch_fetch(query)
    unsplash_imgs = ingestors.unsplash_ingestor.perform_batch_fetch(query)
    photos = pexels_imgs + pixabay_imgs + unsplash_imgs
    insert_imgs_for_review(photos)
    print("Completed processing")

