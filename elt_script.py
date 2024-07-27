import os
from crawlers import results_crawler, channels_crawler
from sql_operations import insert_videos

# Getting some env variables
url_videos = os.environ.get("API_URL_VIDEOS")
url_channels = os.environ.get("API_URL_CHANNELS")
key = os.environ.get("API_KEY")

URI = os.environ.get('POSTGRES_URI')

print("ELT script started...")

# Method that performs the get request to the API to get the top 200 videos
responses = results_crawler(url_videos, key)

# Insert the videos into postgres
insert_videos(responses)
print("videos uploaded to the db.")

# Get info about every channel that has appeared in videos table, i.e every channel encountered from the earlier API responses
channels_crawler(url=url_channels, api_key=key)

print("Done.")




