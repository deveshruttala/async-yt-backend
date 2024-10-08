# from django.contrib import admin
# from api.models import *

# class VideoDataAdmin(admin.ModelAdmin):
#     list_display = ('videoTitle', 'videoId', 'channelTitle','pub_date', 'desc')
#     search_fields = ('channelId','videoId')

# # Register your models here.
# admin.site.register(VideoData, VideoDataAdmin)


from django.contrib import admin
from .models import VideoData

class VideoDataAdmin(admin.ModelAdmin):
    list_display = ('videoTitle', 'videoId', 'channelTitle', 'pub_date', 'desc')
    search_fields = ('channelId', 'videoId')

# Register your models here.
admin.site.register(VideoData, VideoDataAdmin)
