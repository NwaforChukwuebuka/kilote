from django.urls import path, include
from social_django.urls import urlpatterns as social_auth_urls
from .views import (
    UnlinkSocialMediaAccountView,
    linkedin_complete, 
    linkedin_post,
)

urlpatterns = [
    path('linkedin/post/', linkedin_post, name='linkedin_post'),
  # LinkedIn post URL
    path('unlink/<str:platform>/', UnlinkSocialMediaAccountView.as_view(), name='unlink_social_account'),  # Unlink account
    path('social/auth/complete/linkedin-oauth2/', linkedin_complete, name='linkedin_complete'),  # LinkedIn OAuth complete URL
]

# Include the social-auth URLs for handling OAuth logins and completions (e.g., for LinkedIn, Facebook)
urlpatterns += social_auth_urls
