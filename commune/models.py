from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from clone.models import Comment, VideoPost
# Create your models here.
class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_pfp = models.FileField(upload_to='thread_pfps', blank=True, null=True)

class MessaegModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    body = models.CharField(max_length=1000)
    image= models.FileField(upload_to='message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class Notifications(models.Model):
    # notification_type: 1=Like, 2=Comment, 3=Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from', null=True)
    
    # Directly reference the imported models Comment and VideoPost
    post = models.ForeignKey(VideoPost, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


    