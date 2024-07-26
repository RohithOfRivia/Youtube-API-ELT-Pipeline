import requests
import sql_operations
import time

responses = []
def results_crawler(current_url, api_key, next_page_token=''):
    if next_page_token == '' : print("fetching videos...")

    response = requests.get(current_url + api_key + next_page_token)

    if response.status_code != 200:
        print("Error: ", response.status_code)
        return responses
    
    json_response = response.json()
    responses.append(json_response)

    next_page = json_response.get("nextPageToken", 0)

    if next_page != 0:
        print('page flipped...')
        next_page = "&pageToken=" + next_page
        results_crawler(current_url, api_key, next_page)

    return responses


def channels_crawler(url, api_key, next_page_token=''):
    channels = sql_operations.get_channels()

    print('No. of channels to be fetched: ', len(channels))
    print("fetching channel data...")

    

    start = 0
    end = len(channels)
    step = 25

    for chunk in range(start, end, step):
        time.sleep(0.5)
        print('flipping page...')
        full_url = url + api_key

        channels_chunk = channels[chunk:chunk + step]
        # print(channels_chunk)

        for channel in channels_chunk:
            full_url = full_url + '&id=' + channel
   
        response = requests.get(full_url + next_page_token)
        
        if response.status_code != 200:
            print("Error: ", response.status_code)

        json_response = response.json() 

        channel_details = {}
        for channel in json_response['items']:

            channel_details['channel_id'] =  channel.get('id', '')

            snippet = channel.get('snippet', {'empty': 0})

            channel_details['channel_name'] = snippet.get('title', '')
            channel_details['description'] = snippet.get('description', '')
            channel_details['custom_url'] = snippet.get('customUrl', '')
            channel_details['channel_start_date'] = snippet.get('publishedAt', '')

            thumb = snippet.get('thumbnails', {'empty': 0})
            channel_details['thumnail_url'] = thumb.get('high', thumb.get('default', ''))
            statistics = channel.get('statistics', {'empty': 0})

            channel_details['views'] = statistics.get('viewCount', '0')
            channel_details['subs'] = statistics.get('subscriberCount', '0')
            channel_details['video_count'] = statistics.get('videoCount', '0')

            # channel_details['topic_ids'] = channel['topicDetails'].get('topicIds', {'empty': 0})
            # channel_details['topic_categories'] = channel['topicDetails'].get('topicCategories', '0')
            channel_details['kids'] =  channel['status'].get('madeForKids', '0')

            # print(channel_details)
            sql_operations.insert_channels(channel_details=channel_details)

            
    return