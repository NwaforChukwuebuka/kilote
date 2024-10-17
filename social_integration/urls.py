from django.urls import path, include
from social_django.urls import urlpatterns as social_auth_urls
from .views import (
    unlink_social_account,
    linkedin_complete, 
    linkedin_post,
    post_to_twitter_view,
)
from . import views


urlpatterns = [
    path('linkedin/post/', linkedin_post, name='linkedin_post'),
  # LinkedIn post URL
    path('unlink/<str:platform>/', unlink_social_account, name='unlink_social_account'),
    path('social/auth/complete/linkedin-oauth2/', linkedin_complete, name='linkedin_complete'),  # LinkedIn OAuth complete URL
    path('twitter/connect/', views.twitter_connect, name='twitter_connect'),
    path('twitter/callback/', views.twitter_callback, name='twitter_callback'),
    path('post_to_twitter/', post_to_twitter_view, name='post_to_twitter_view'),
]


# Include the social-auth URLs for handling OAuth logins and completions (e.g., for LinkedIn, Facebook)
urlpatterns += social_auth_urls
