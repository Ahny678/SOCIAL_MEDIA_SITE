from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from clone.models import Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'name' ,'bio']

class CommentForm(forms.ModelForm):
    comment=forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={
            'rows' : 3,
            'placeholder':'make a comment...'
        })

    )
    class Meta:
        model = Comment
        fields = ['comment']