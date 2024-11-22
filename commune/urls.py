from django.urls import path
from . import views
from .views import ListThreads, CreateThread, ThreadView, CreateMessage, PostNotification,FollowNotification

urlpatterns = [
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/createthread/', CreateThread.as_view(), name='createthread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/createmessage/', CreateMessage.as_view(), name='createmessage'),
    path('notifications', views.notifs, name='notifs'),
    path('follow/<int:notification_pk>/<int:profile_pk>/', FollowNotification.as_view(), name='followView'),
    path('post/<int:notification_pk>/<int:post_pk>/', views.PostNotification.as_view(), name='postView'),


]