
import requests
from django.shortcuts import render
from api.models import VideoData
from fampay import settings

def schedulee():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': 'learn python',
        'publishedAfter': '2022-01-01T00:00:00Z',
        'key': settings.YOUTUBE_API,
    }

    r = requests.get(search_url, params=params)
    data = r.json()  # Parse the JSON response
    
    # Check if 'items' exists in the response
    if 'items' in data:
        for item in data['items']:
            # Check if 'id' and 'videoId' exist
            if 'id' in item and 'videoId' in item['id']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                channel_title = item['snippet']['channelTitle']
                # Save to the database
                VideoData.objects.create(
                    videoId=video_id,
                    videoTitle=video_title,
                    channelTitle=channel_title,
                )
            else:
                print("No videoId found for item:", item)
    else:
        print("No items found in response:", data)
