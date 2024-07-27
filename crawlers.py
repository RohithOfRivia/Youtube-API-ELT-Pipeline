import requests
import sql_operations
import time

'''list that stores every item from the HTTP response. Each response can only show a maximum of 50 list items. 
The rest of the items must be gathered with another API request with the next page parameter. So each response 
(there will 4 in total) is converted into json and stored in the responses variable.   '''

# Used by results_crawler() to store responses
responses = []

# Method to fetch top 200 videos
def results_crawler(current_url, api_key, next_page_token=''):

    # Prints this on the first API call  
    if next_page_token == '' : print("fetching videos...")

    # Get request for the API
    response = requests.get(current_url + api_key + next_page_token)

    # Make sure the response is okay
    if response.status_code != 200:
        print("Error: ", response.status_code)
        return responses
    
    # Convert response to json and store in responses
    json_response = response.json()
    responses.append(json_response)

    # Get the next page param for the next API call
    next_page = json_response.get("nextPageToken", 0)

    # Indicate the API call with the next page param   
    if next_page != 0:
        print('page flipped...')
        next_page = "&pageToken=" + next_page

        # Calling the method again to get the response for the next page
        results_crawler(current_url, api_key, next_page)

    # Return all responses
    return responses

# Method to get info about all the channels that appear in the database
def channels_crawler(url, api_key, next_page_token=''):

    # Helper method to get all channels in the database through a select statement 
    channels = sql_operations.get_channels()

    # Some helpful prints
    print('No. of channels to be fetched: ', len(channels))
    print("fetching channel data...")

    
    ''' The API only supports get requests that request for the details of 25 channels per request.
      So, splitting them into chunks of 25 before making the request.  '''
     
    start = 0
    end = len(channels)
    step = 25

    # Iterate through the chunks to get channels details

    for chunk in range(start, end, step):

        # Small waiting period to prevent API issues
        time.sleep(0.5)
        print('flipping page...')
        full_url = url + api_key

        # Indexing into the chunk
        channels_chunk = channels[chunk:chunk + step]

        # Adding all channels in the chunk into the url params
        for channel in channels_chunk:
            full_url = full_url + '&id=' + channel

        # Get request
        response = requests.get(full_url + next_page_token)
        
        # Make sure the response is okay
        if response.status_code != 200:
            print("Error: ", response.status_code)

        # Convert to JSON
        json_response = response.json() 

        # Putting the details of channels into a dictionary to send it to a method that inserts them into the db
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

            channel_details['kids'] =  channel['status'].get('madeForKids', '0')


            ''' helper method that inserts each channel into the database. The number of channels are fairly low,
                so we can get away with only doing one insert at a time.'''
            
            sql_operations.insert_channels(channel_details=channel_details)

            
    return