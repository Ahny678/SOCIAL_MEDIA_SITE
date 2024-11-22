from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.db.models import Q
from .models import ThreadModel, MessaegModel, Notifications
from clone.models import VideoPost, Comment
from users.models import Profile
from .forms import ThreadForm, MessageForm
from django.contrib.auth.models import User
from django.urls import reverse



# Create your views here.
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads
        }
        return render(request, 'commune/inbox.html', context)
    

#this will prolly be triggered when i click message
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form' :form
        }
        return render(request, 'feed/feeder_profile.html', context)
 
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
        
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread=ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread=ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            #create thread if it doesnt exist
            if form.is_valid():
                thread = ThreadModel(
                    user = request.user,
                    receiver=receiver,
                     receiver_pfp = receiver.profile.image 
                )
                thread.save()
                return redirect('thread', pk=thread.pk )
        except:
            return redirect('FeederProfilePage', username=username)

class ThreadView(View):
    def get(self, request,pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        messages_list = MessaegModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread' : thread, 
            'form' : form, 
            'messages_list' : messages_list
        }
        return render(request, 'commune/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        message = MessaegModel(
        thread= thread,
        sender_user= request.user,
        receiver_user=receiver,
        body=request.POST.get('message')
        )
        message.save()
        return redirect('thread', pk=pk)

def notifs(request):
    to_user = request.user
    notifications = Notifications.objects.filter(to_user=request.user, user_has_seen=False).order_by('-date')
    context = {
        'notifications': notifications
    }
    return render(request, 'commune/notifs.html', context)

class PostNotification(View):
    def get(self,request, notification_pk, post_pk, *args, **kwargs):
        notification = Notifications.objects.get(pk=notification_pk)   
        post = VideoPost.objects.get(pk=post_pk)

        notification.user_has_seen=True   
        notification.save()    
        return redirect(reverse('mv', kwargs={'pk': post.pk}))
                                                                                                                                                                                                                                                                                               

class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        # Fetch notification and profile
        notification = get_object_or_404(Notifications, pk=notification_pk)
        profile = get_object_or_404(Profile, pk=profile_pk)

        # Mark notification as seen
        notification.user_has_seen = True
        notification.save()

        # Redirect to the profile page
        return redirect(reverse('FeederProfilePage', kwargs={'username': profile.user.username}))   












     
    
