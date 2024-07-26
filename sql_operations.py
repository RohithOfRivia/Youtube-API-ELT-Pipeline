import psycopg2
import os
import json
from datetime import datetime, timezone

URI = os.environ.get('POSTGRES_URI')
TABLE = 'videos'



def insert_videos(responses, test=False):
    videos_uploaded_count = 0
    COLS =  'req_date, daily_rank, title, video_id, publish_date, channel_id, descr, thumbnail_link, dimension, views, likes, comments, favourite_count, category'

    insert_query = f"INSERT INTO videos ({COLS}) "+ """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                    """
    

    # Establish a connection to the database
    try:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
    except Exception as e: 
        print(e)

    now_utc = datetime.now(timezone.utc)

    # Format the time string with timezone offset
    formatted_time = now_utc.strftime("%Y-%m-%dT%H:%M:%S")
    page = 0
    
    if (test == True):
        responses = json.load(open("data.json", 'r'))

    for j in range(len(responses)):

        rank_start = 50 * page
        response = responses[j] 

        for i in range(len(response['items'])):

            rank = rank_start + i + 1
            current_video = response['items'][i]
        
            try:

                cursor.execute(insert_query, (formatted_time, rank, current_video['snippet']['title'], current_video['id'], current_video['snippet']['publishedAt'], current_video['snippet']['channelId'], current_video['snippet']['description'], current_video['snippet']['thumbnails'].get('maxres', current_video['snippet']['thumbnails'].get('default', {'url': ''}))['url'], current_video['contentDetails']['dimension'], current_video['statistics']['viewCount'], current_video['statistics']['likeCount'], current_video['statistics'].get('commentCount', -1), current_video['statistics']['favoriteCount'], current_video['snippet']['categoryId']))

            except psycopg2.Error as e:
                print(f"Error inserting data: {e}")


            connection.commit()
            videos_uploaded_count += 1
        page += 1
        
    cursor.close()
    connection.close()
    # print('No. of inserts attempted: ', videos_uploaded_count)

    return

def get_channels():
    channels = []
    select_query = '''SELECT videos.channel_id
                FROM videos
                LEFT JOIN channels ON videos.channel_id = channels.channel_id
                WHERE channels.channel_id IS NULL'''
                
    # Establish a connection to the database
    try:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
    except Exception as e: 
        print(e)


    # Fetch all results from the executed SELECT statement
    cursor.execute(select_query)
    records = cursor.fetchall()

    # Process the fetched results
    for record in records:
        channels.append(record[0])

    cursor.close()
    connection.close()

    return channels 

def insert_channels(channel_details={}):
    cols =  'channel_id, channel_name, channel_username, descr, channel_start_date, subs, views, video_count, kids_channel, profile_picture_url'

    insert_query = f"INSERT INTO channels ({cols}) "+ """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                    """
    

    try:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
    except Exception as e: 
        print(e)

    try:
        cursor.execute(insert_query, (channel_details['channel_id'], channel_details['channel_name'], channel_details['custom_url'], channel_details['description'], channel_details['channel_start_date'], channel_details['subs'], channel_details['views'], channel_details['video_count'], channel_details['kids'], channel_details['thumnail_url']['url']))
        connection.commit() 


    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")   

    cursor.close()


    
    connection.close()
    
    return
