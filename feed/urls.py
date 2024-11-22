from django.urls import path
from . import views
from .views import(FeedVideoListView, AddFollower, RemoveFollower, 
                   FeedVideoDetailView, AddLike, AddDislike, UserSearch, AddCommentDislike, AddCommentLike)

urlpatterns = [
    path('feed/', FeedVideoListView.as_view(), name='feed'),
     path('FeederProfilePage/<str:username>/', views.FeederProfilePage, name='FeederProfilePage'),
     path('FeederProfile/', views.FeederProfile, name='FeederProfile'),
     path('FeedVideoDetailView/<int:pk>/', views.FeedVideoDetailView.as_view(), name='FeedVideoDetailView'),
     path('FeedVideoDetailView/<int:post_pk>/CommentDeleteView/<int:pk>/', views.CommentDeleteView.as_view(), name='CommentDeleteView'),
     path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='addfollower'),
     path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='removefollower'),
     path('feed/addlike/<int:pk>/', views.AddLike.as_view(), name='like'),
     path('feed/dislike/<int:pk>/', views.AddDislike.as_view(), name='dislike'),
     path('feed/addcommentlike/<int:pk>/', views.AddCommentLike.as_view(), name='like_comment'),
     path('feed/dislikecomment/<int:pk>/', views.AddCommentDislike.as_view(), name='dislike_comment'),
     path('ProSearcher/', views.GoToSearch, name='gts'),
     path('search/',views.UserSearch.as_view(), name='search')
]