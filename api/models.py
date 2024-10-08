

from django.db import models

class VideoData(models.Model):
    channelId = models.CharField(max_length=255, blank=True, null=True)  # Allow NULL values if needed
    videoId = models.CharField(max_length=255, default=None)
    videoTitle = models.CharField(max_length=255, default=None)
    desc = models.TextField(blank=True, null=True)  # Optional description
    channelTitle = models.CharField(max_length=255, blank=True, null=True)  # Optional channel title
    pub_date = models.DateTimeField(auto_now_add=True)
    thumb_url = models.URLField(default=None,blank=True, null=True)  # Required field

    def __str__(self):
        return self.videoTitle

