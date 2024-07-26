import os
from crawlers import results_crawler, channels_crawler
from sql_operations import insert_videos

url_videos = os.environ.get("API_URL_VIDEOS")
url_channels = os.environ.get("API_URL_CHANNELS")
key = os.environ.get("API_KEY")

URI = os.environ.get('POSTGRES_URI')
TABLE = 'videos'
COLS =  'req_date, daily_rank, title, video_id, publish_date, channel_id, descr, thumbnail_link, dimension, views, likes, comments, favourite_count, category'

print("ELT script started...")

responses = results_crawler(url_videos, key)
insert_videos(responses)
print("videos uploaded to the db.")
channels_crawler(url=url_channels, api_key=key)

print("Done.")




