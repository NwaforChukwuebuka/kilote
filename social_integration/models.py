from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from post_management.models import Post  # Import the Post model

class SocialMediaAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who owns the account
    platform_name = models.CharField(max_length=100)  # e.g., 'LinkedIn', 'Twitter', etc.
    profile_image = models.ImageField(upload_to='images/profile_images/', blank=True, null=True)  # Profile image
    full_name = models.CharField(max_length=255, blank=True, null=True)  # User's full name
    access_token = models.CharField(max_length=255)  # OAuth access token
    access_token_secret = models.CharField(max_length=255, default='', blank=True)  # Default empty string
    screen_name = models.CharField(max_length=100, blank=True, null=True)  # e.g., Twitter screen name (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when account was connected
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when account details were last updated

    def __str__(self):
        return f"{self.full_name or self.screen_name} - {self.platform_name}"


class SocialMediaPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Reference to the Post
    social_media_account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)  # Reference to the social media account
    posted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was made on social media
    post_status = models.CharField(max_length=50, default='Pending')  # Status of the post (e.g., Pending, Posted, Failed)

    def __str__(self):
        return f"Post {self.post.id} on {self.social_media_account.platform_name} - Status: {self.post_status}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    twitter_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_token_secret = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to create a UserProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
