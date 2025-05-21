from django import forms
from .models import Message, File, Profile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['recipient', 'file']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
