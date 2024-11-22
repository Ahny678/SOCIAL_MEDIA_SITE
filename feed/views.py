from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View
from clone.models import VideoPost, Comment
from commune.models import Notifications
from users.models import Profile
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, DeleteView
from users.forms import CommentForm
from django.db.models import Q

# Create your views here.
# class FeedVideoListView(View):
#     def get(self, request, *args, **kwargs):
#         feed_videos = VideoPost.objects.all().order_by('-post_date')
#         paginator = Paginator(feed_videos, 1)
#         comments = Comment.object.filter()
#         # Get the page number from the request
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context = {
       
#          'page_obj':page_obj
#      }  
   
#         return render(request, 'feed/feed_videos.html', context)

class FeedVideoListView(View):
    def get(self, request, *args, **kwargs):
        # Fetch all videos and order by post date
        feed_videos = VideoPost.objects.all().order_by('-post_date')

        # Paginate the videos (assuming 1 video per page)
        paginator = Paginator(feed_videos, 1)

        # Get the current page number from the request
        page_number = request.GET.get('page')

        # Get the videos for the current page
        page_obj = paginator.get_page(page_number)

        # Get the current video post (there's one video per page)
        current_video = page_obj.object_list[0] if page_obj.object_list else None

        # If there's a current video, fetch its related comments
        comments = Comment.objects.filter(video_post=current_video) if current_video else []

        context = {
            'page_obj': page_obj,
            'comments': comments,  
            }

        # Render the feed_videos.html template with the context
        return render(request, 'feed/feed_videos.html', context)

    

def FeederProfilePage(request, username):
    try:
        # Get the user by username
        user_obj = User.objects.get(username=username)
        # Fetch the profile for that user
        feed_profile = Profile.objects.get(user=user_obj)
        followers = feed_profile.followers.all()
        follower_count = len(followers)

        if len(followers) == 0:
            is_following=False
        

        for follower in followers:
            if follower == request.user:
                is_following = True
            else:
                is_following = False
        
        
        # Prepare the context to be passed to the template
        context = {
            'feed_profile': feed_profile,
            'follower_count':follower_count,
            'is_following':is_following
        }
        return render(request, 'feed/feeder_profile.html', context)
    except User.DoesNotExist:
        return render(request, '404.html', {'error': 'User not found'})
    except Profile.DoesNotExist:
        return render(request, '404.html', {'error': 'Profile not found'})



def FeederProfile(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        try:
            print(f"Redirecting to /FeederProfilePage/{username}/")  # Debug print
            # Return a JSON response with the URL to redirect to
            return JsonResponse({'redirect_url': f'/FeederProfilePage/{username}/'})
        except User.DoesNotExist:
        
            return JsonResponse({'error': 'User does not exist'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class FeedVideoDetailView(View):
    def get(self, request,pk, *args,**kwargs):
        post = VideoPost.objects.get(pk=pk)
        comment_form = CommentForm()
        comments = Comment.objects.filter(video_post=post).order_by('-created_on')

        context={
            'post': post,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, 'feed/feed_detail.html', context)

    def post(self, request,pk, *args,**kwargs):
        post = VideoPost.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.video_post = post
            new_comment.save()
        comments = Comment.objects.filter(video_post=post).order_by('-created_on')
        notification = Notifications.objects.create(notification_type=2, from_user=request.user, to_user=post.user, post=post)
        

        context={
            'post': post,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, 'feed/feed_detail.html', context)

 
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'feed/comment_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video_post'] = self.get_object().video_post  # Pass video_post to the template
        return context

    def get_success_url(self):
        video_post = self.get_object().video_post
        return reverse_lazy('FeedVideoDetailView', kwargs={'pk': video_post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

  

    
class RemoveFollower(LoginRequiredMixin,View):
    def post(self, request, pk, *args,**kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        username = profile.user

        return redirect(reverse('FeederProfilePage' ,args=[username]) )
    
class AddFollower(LoginRequiredMixin,View):
    def post(self, request, pk, *args,**kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        username = profile.user
        notification = Notifications.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect(reverse('FeederProfilePage' ,args=[username]) )

# Add Post Like
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(VideoPost, pk=pk)

        # Remove dislike if it exists
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)

        # Toggle like
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)  # Unlike if liked
        else:
            post.likes.add(request.user)  # Like if not already liked
            notification = Notifications.objects.create(notification_type=1, from_user=request.user, to_user=post.user, post=post)

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)

# Add Post Dislike
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(VideoPost, pk=pk)

        # Remove like if it exists
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

        # Toggle dislike
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)  # Undislike if disliked
        else:
            post.dislikes.add(request.user)  # Dislike if not already disliked

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)
    
# Add Comment Like
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)

        # Remove dislike if it exists
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)

        # Toggle like
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)  # Unlike if liked
        else:
            comment.likes.add(request.user)  # Like if not already liked

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)

# Add Comment Dislike
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)

        # Remove like if it exists
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)

        # Toggle dislike
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)  # Undislike if disliked
        else:
            comment.dislikes.add(request.user)  # Dislike if not already disliked

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)



def GoToSearch(request):
    return render(request, 'feed/search.html')

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')  # Default to an empty string if no query is passed
        if query:
            profile_list = Profile.objects.filter(Q(user__username__icontains=query))
        else:
            profile_list = Profile.objects.none()  # Return an empty queryset if no query

        context = {
            'profile_list': profile_list
        }
        return render(request, 'feed/search.html', context)

