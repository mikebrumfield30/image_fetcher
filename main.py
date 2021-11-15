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

# [
# 	{
# 		"plant": 'plant name',
# 		'term': 'query'
# 	}
# ]
def remove_spaces_and_map_queries(query_map):
    no_spaces = []
    for _ in query_map:
        no_spaces.append((remove_spaces(_['plant']), _['term']))
    return no_spaces


def perform_processing(input):
    for plant, term in input:
        pexels_imgs = ingestors.pexels_ingestor.perform_batch_fetch(term, plant)
        pixabay_imgs = ingestors.pixabay_ingestor.perform_batch_fetch(term, plant)
        unsplash_imgs = ingestors.unsplash_ingestor.perform_batch_fetch(term, plant)
        photos = pexels_imgs + pixabay_imgs + unsplash_imgs
        insert_imgs_for_review(photos)


def read_input_file(filename):
    try:
        f = open(filename)
        data = json.load(f)
        return remove_spaces_and_map_queries(data)
    except Exception as e:
        print(e.with_traceback())
        print("file not found")
        sys.exit(1)


def list_of_queries_to_tuples(queries):
    tuples = []
    for q in queries:
        tuples.append((q, q))
    return tuples


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to get some free images from variety of API's and store "
                                                 "metadata in mongo")
    parser.add_argument('--query', type=str, nargs=1, required=False, help="Search term")
    parser.add_argument('--input_file', type=str, required=False,  help='Search file. Using a file allows mapping queries to plants')

    args = parser.parse_args()
    if args.input_file:
        data = read_input_file(args.input_file)
        perform_processing(data)
        print("Completed processing")
    else:
        query = args.query[0]
        list_of_queries = query.split(',')
        r = map(remove_spaces, list_of_queries)
        tuples = list_of_queries_to_tuples(list(r))
        perform_processing(tuples)
        print("Completed processing")

