from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'video_url', 'image', 'social_media_accounts']  # Include 'image' field here
