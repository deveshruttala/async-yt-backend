from django.shortcuts import render
import requests
from api.models import VideoData
from fampay import settings
from datetime import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'index.html')

def search(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search' # search url for youtube data api search

    search_query = request.GET.get('query', 'trending')


    params = { # specifying the parameters for the search
        'part': 'snippet',
        'q': search_query,
        'type':'video',
        'publishedAfter': '2022-05-01T00:00:00Z',
        'maxResults': '10',
        'order':'date',
        'key': settings.YOUTUBE_API,
    }
    query = request.GET.get('query', 'trending')

    r = requests.get(search_url, params = params)
    res = r.json() #converting to json object

    try:
        if(res['error']['code'] == 403 or res['error']['code'] == 400): # checking if the data limit has exhausted for the API key
            print("New API Key required")

            params = {
                'part': 'snippet',
                'q': query,
                'type':'video',
                'publishedAfter': '2022-05-01T00:00:00Z',
                'maxResults': '10',
                'order':'date',
                'key': settings.YOUTUBE_API_2, # if the previous API key limit is exhaused, we use the next available API key
            }

            r = requests.get(search_url, params= params)
            res = r.json()

    except KeyError:
        pass
    
    now = datetime.now()    # datetime object containing current date and time

    jsonn = res['items']
    nextPage = res['nextPageToken'] # getting the next Page Token for pagination

    for item in jsonn:
        d1 = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
        d1 = d1 + + timedelta(minutes = 330) # adding 330 minutes to the time to get the correct timezone
        item['snippet']['publishedAt'] = d1

        if VideoData.objects.filter(videoId = item['id']['videoId']).exists(): # checking if the video is also in the database
            pass
        else:
            # adding the video to the database with necessary details
            VideoData.objects.create(channelId = item['snippet']['channelId'], videoId = item['id']['videoId'], 
            videoTitle = item['snippet']['title'], desc = item['snippet']['description'], 
            channelTitle = item['snippet']['channelTitle'], pub_date = item['snippet']['publishedAt'], 
            thumb_url = item['snippet']['thumbnails']['high']['url']).save() # saving to the database

    context = {'json': jsonn, 'nextPage': nextPage}
    return render(request, 'index.html', context)

@csrf_exempt
def pagination(request, PageToken):
    filter_duration = request.POST['duration'] # getting the Video Duration if the user has selected any filter
    if filter_duration == '':
        filter_duration = 'any' # if the user has not selected any filter, then the filter_duration will be 'any'
    
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    
    search_query = request.GET.get('query', 'trending')


    params = {
        'part': 'snippet',
        'q': search_query,
        'type':'video',
        'publishedAfter': '2022-05-01T00:00:00Z',
        'maxResults': '10',
        'order':'date',
        'pageToken': PageToken,
        'videoDuration': filter_duration,
        'key': settings.YOUTUBE_API,
    }

    r = requests.get(search_url, params = params)
    res = r.json()
    
    try:
        if(res['error']['code'] == 403 or res['error']['code'] == 400):
            print("New API Key required")

            params = {
                'part': 'snippet',
                'q': search_query,
                'type':'video',
                'publishedAfter': '2022-05-01T00:00:00Z',
                'maxResults': '10',
                'order':'date',
                'pageToken': PageToken,
                'videoDuration': filter_duration,
                'key': settings.YOUTUBE_API_2,
            }

            r = requests.get(search_url, params= params)
            res = r.json()

    except KeyError:
        pass

    jsonn = res['items']
    nextPage = res['nextPageToken']
    try:
        prevPage = res['prevPageToken']

        for item in jsonn:
            d1 = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            d1 = d1 + + timedelta(minutes = 330)
            item['snippet']['publishedAt'] = d1

            if VideoData.objects.filter(videoId = item['id']['videoId']).exists(): # checking if the video is also in the database
                pass
            else:
                # adding the video to the database with necessary details
                VideoData.objects.create(channelId = item['snippet']['channelId'], videoId = item['id']['videoId'], 
                videoTitle = item['snippet']['title'], desc = item['snippet']['description'], 
                channelTitle = item['snippet']['channelTitle'], pub_date = item['snippet']['publishedAt'], 
                thumb_url = item['snippet']['thumbnails']['high']['url']).save()


        context = {'json': jsonn, 'nextPage': nextPage, 'prevPage': prevPage, 'filter_duration': filter_duration}
        return render(request, 'index.html', context)

    except KeyError:
        for item in jsonn:
            d1 = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            d1 = d1 + + timedelta(minutes = 330)
            item['snippet']['publishedAt'] = d1

            if VideoData.objects.filter(videoId = item['id']['videoId']).exists(): # checking if the video is also in the database
                pass
            else:
                # adding the video to the database with necessary details
                VideoData.objects.create(channelId = item['snippet']['channelId'], videoId = item['id']['videoId'], 
                videoTitle = item['snippet']['title'], desc = item['snippet']['description'], 
                channelTitle = item['snippet']['channelTitle'], pub_date = item['snippet']['publishedAt'], 
                thumb_url = item['snippet']['thumbnails']['high']['url']).save()


        context = {'json': jsonn, 'nextPage': nextPage,  'filter_duration': filter_duration}
        return render(request, 'index.html', context)

def filter_video(request):
    filter_duration = request.POST['duration']

    search_url = 'https://www.googleapis.com/youtube/v3/search'

    search_query = request.GET.get('query', 'trending')

    params = {
        'part': 'snippet',
        'q': search_query,
        'type':'video',
        'publishedAfter': '2022-05-01T00:00:00Z',
        'maxResults': '10',
        'order':'date',
        'videoDuration': filter_duration,
        'key': settings.YOUTUBE_API,
    }

    r = requests.get(search_url, params = params)
    res = r.json()

    try:
        if(res['error']['code'] == 403 or res['error']['code'] == 400):
            print("New API Key required")

            params = {
                'part': 'snippet',
                'q': 'trending',
                'type':'video',
                'publishedAfter': '2022-05-01T00:00:00Z',
                'maxResults': '10',
                'order':'date',
                'videoDuration': filter_duration,
                'key': settings.YOUTUBE_API_2,
            }

            r = requests.get(search_url, params = params)
            res = r.json()

    except KeyError:
        pass

    jsonn = res['items']
    nextPage = res['nextPageToken']

    for item in jsonn:
        d1 = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
        d1 = d1 + + timedelta(minutes = 330)
        item['snippet']['publishedAt'] = d1

        if VideoData.objects.filter(videoId = item['id']['videoId']).exists(): # checking if the video is also in the database
            pass
        else:
            # adding the video to the database with necessary details
            VideoData.objects.create(channelId = item['snippet']['channelId'], videoId = item['id']['videoId'], 
            videoTitle = item['snippet']['title'], desc = item['snippet']['description'], 
            channelTitle = item['snippet']['channelTitle'], pub_date = item['snippet']['publishedAt'], 
            thumb_url = item['snippet']['thumbnails']['high']['url']).save()

    context = {'json': jsonn, 'nextPage': nextPage, 'filter_duration': filter_duration}
    return render(request, 'index.html', context)