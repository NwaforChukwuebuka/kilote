# social_integration/backends.py
from social_core.backends.linkedin import LinkedinOAuth2

class CustomLinkedinOAuth2(LinkedinOAuth2):
    def get_scope(self, request=None):
        # Return only the desired scopes
        return ['profile', 'email', 'w_member_social', 'openid']
