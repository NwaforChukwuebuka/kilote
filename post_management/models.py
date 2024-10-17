from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    content = models.TextField(blank=True, null=True)  # Text content of the post
    video_url = models.URLField(blank=True, null=True)  # URL of the video (if applicable)
    image = models.ImageField(upload_to='images/posts/', blank=True, null=True)  # Image upload
    social_media_accounts = models.JSONField(blank=True, null=True)  # List of social media accounts
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user who made the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the post is last updated

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"



