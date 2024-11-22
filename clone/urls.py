from django.urls import path
from . import views
from .views import (
    PostVideoListView,
      PostVideoDetailView, 
      PostVideoCreateView,
      PostVideoUpdateView,
      PostVideoDeleteView,
      MyComments,
)

urlpatterns=[
    path('base', views.base, name='base'),
    path('myVideos/', PostVideoListView.as_view(), name='myVideos'),
    path('mv/<int:pk>/', PostVideoDetailView.as_view(), name='mv'),
    path('create/', PostVideoCreateView.as_view(), name='create'), 
    path('mv/<int:pk>/update', PostVideoUpdateView.as_view(), name='updatePost'),
    path('mv/<int:pk>/delete', PostVideoDeleteView.as_view(), name='deletePost'),
    path('mv/<int:pk>/MyComments/', views.MyComments.as_view(), name='mycomments'),
    


]