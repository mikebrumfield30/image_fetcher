import json
import boto3
import ingestors.unsplash_ingestor as ui
import ingestors.pexels_ingestor as pi
import ingestors.pixabay_ingestor
from datetime import datetime
import argparse


def upload_json_to_s3(json_dict, s3_filename, filename, bucket='777377719930-synthesis-assests-s3'):
    tmp_file = open(f'/tmp/{filename}', 'x')
    tmp_file.write(json.dumps(json_dict))
    tmp_file.close()
    client = boto3.client('s3')
    r = client.upload_file(
        f'/tmp/{filename}',
        bucket,
        s3_filename
    )
    return r


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to get some free images from variety of API's and store "
                                                 "metadata in s3")
    parser.add_argument('--query', type=str, nargs=1, required=True, help="Search term")

    args = parser.parse_args()
    query = args.query[0]
    query_no_space = query.strip().replace(' ', '_')
    pexels_imgs = ingestors.pexels_ingestor.perform_batch_fetch('aloe')
    pixabay_imgs = ingestors.pixabay_ingestor.perform_batch_fetch('aloe')
    photos = pexels_imgs + pixabay_imgs
    timestamp = datetime.today().strftime('%Y-%m-%d')
    file = f"raw_photos_for_review/{timestamp}-{query_no_space}.json"
    r = upload_json_to_s3(photos, file, f'{timestamp}-{query_no_space}.json')
    print("Completed processing")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
