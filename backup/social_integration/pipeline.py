# In a file like social_integration/pipeline.py
from social_core.backends.linkedin import LinkedinOAuth2

def set_custom_linkedin_scope(backend, details, response, *args, **kwargs):
    if isinstance(backend, LinkedinOAuth2):
        backend.DEFAULT_SCOPE = ['openid', 'profile', 'w_member_social', 'email']
