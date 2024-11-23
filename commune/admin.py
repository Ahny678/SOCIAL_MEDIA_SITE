from django.contrib import admin
from .models import Notifications, MessaegModel, ThreadModel
# Register your models here.

admin.site.register(Notifications)
admin.site.register(MessaegModel)
admin.site.register(ThreadModel)