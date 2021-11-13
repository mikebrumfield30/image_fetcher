import json
import boto3
import ingestors.unsplash_ingestor
import ingestors.pexels_ingestor
import ingestors.pixabay_ingestor
from datetime import datetime
from mongo import insert_imgs_for_review
import argparse
import sys


def remove_spaces(query):
    return query.strip().replace(' ', '_')


def perform_processing(input):
    for _ in input:
        pexels_imgs = ingestors.pexels_ingestor.perform_batch_fetch(_)
        pixabay_imgs = ingestors.pixabay_ingestor.perform_batch_fetch(_)
        unsplash_imgs = ingestors.unsplash_ingestor.perform_batch_fetch(_)
        photos = pexels_imgs + pixabay_imgs + unsplash_imgs
        insert_imgs_for_review(photos)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to get some free images from variety of API's and store "
                                                 "metadata in mongo")
    parser.add_argument('--query', type=str, nargs=1, required=True, help="Search term")

    args = parser.parse_args()
    query = args.query[0]
    list_of_queries = query.split(',')
    r = map(remove_spaces, list_of_queries)
    perform_processing(list(r))
    print("Completed processing")

