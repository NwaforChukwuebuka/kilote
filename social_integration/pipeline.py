# In a file like social_integration/pipeline.py
from social_core.backends.linkedin import LinkedinOAuth2

def set_custom_linkedin_scope(backend, details, response, *args, **kwargs):
    if isinstance(backend, LinkedinOAuth2):
        backend.DEFAULT_SCOPE = ['openid', 'profile', 'w_member_social', 'email']

def save_twitter_token(strategy, details, user=None, *args, **kwargs):
    if user and kwargs['response']:
        profile = user.userprofile
        # profile.twitter_token = kwargs['response']['oauth_token']
        # profile.twitter_token_secret = kwargs['response']['oauth_token_secret']
        profile.save()