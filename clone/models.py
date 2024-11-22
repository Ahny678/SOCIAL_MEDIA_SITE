from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class VideoPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='post_videos/')
    thumbnail = models.FileField(upload_to='video_thumbnails/')
    description = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return f"{self.user.username}'s Post" 
    
    def get_absolute_url(self):
        return reverse('mv', kwargs={'pk' : self.pk})

class Comment(models.Model):
    comment=models.TextField()
    created_on=models.DateTimeField(default=timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    video_post= models.ForeignKey(VideoPost, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='commentlikes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='commentdislikes')

