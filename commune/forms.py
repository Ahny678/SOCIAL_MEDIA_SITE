from django import forms

class ThreadForm(forms.Form):
    username=forms.CharField(label='',max_length=255)

class MessageForm(forms.Form):
    message=forms.CharField(label='',max_length=255)