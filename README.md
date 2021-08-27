# Free Image Fetcher

Free Image fetcher is part of content creation for synthesis. It downloads images of plants to be reviewed for approval on the site [Synthesis](https://plantsynthesis.com)

This project fetches images from pexels, pixabay and unsplash API's. API keys for each are stored in AWS parameter store. Metadata for fetched images is stored in a json in mongoDB

## Execution

The script takes one argument, --query, that specifies what images to search for. 

## Usage

```bash
python3 main.py --query <search_term>
# E.g.
python3 main.py --query aloe
```
