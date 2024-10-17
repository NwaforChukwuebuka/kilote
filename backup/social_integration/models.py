from django.db import models
from django.contrib.auth.models import User
from post_management.models import Post  # Import the Post model

class SocialMediaAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who owns the account
    platform_name = models.CharField(max_length=100)  # e.g., 'LinkedIn', 'Twitter', etc.
    profile_image = models.ImageField(upload_to='images/profile_images/', blank=True, null=True)  # Profile image
    full_name = models.CharField(max_length=255, blank=True, null=True)  # User's full name
    access_token = models.CharField(max_length=255)  # Access token for authentication
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when account was connected
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when account details were last updated

    def __str__(self):
        return f"{self.full_name} - {self.platform_name}"

class SocialMediaPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Reference to the Post
    social_media_account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)  # Reference to the social media account
    posted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was made on social media
    post_status = models.CharField(max_length=50, default='Pending')  # Status of the post (e.g., Pending, Posted, Failed)

    def __str__(self):
        return f"Post {self.post.id} on {self.social_media_account.platform_name} - Status: {self.post_status}"

