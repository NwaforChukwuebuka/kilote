"""
LinkedIn OpenID Connect backend, docs at:
    https://python-social-auth.readthedocs.io/en/latest/backends/linkedin.html
"""

import datetime
from calendar import timegm
from social_core.backends.open_id_connect import OpenIdConnectAuth
from social_core.exceptions import AuthCanceled, AuthTokenError

from .oauth import BaseOAuth2


class LinkedinOpenIdConnect(OpenIdConnectAuth):
    """
    LinkedIn OpenID Connect backend. OAuth2 has been deprecated as of August 1, 2023.
    https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2?context=linkedin/consumer/context
    """

    name = "linkedin-openidconnect"
    OIDC_ENDPOINT = "https://www.linkedin.com/oauth"
    TOKEN_ENDPOINT_AUTH_METHOD = "client_secret_post"

    def validate_claims(self, id_token):
        """Validate the OpenID token without the nonce validation."""
        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())

        if "nbf" in id_token and utc_timestamp < id_token["nbf"]:
            raise AuthTokenError(self, "Incorrect id_token: nbf")

        iat_leeway = self.setting("ID_TOKEN_MAX_AGE", self.ID_TOKEN_MAX_AGE)
        if utc_timestamp > id_token["iat"] + iat_leeway:
            raise AuthTokenError(self, "Incorrect id_token: iat")


class LinkedinOAuth2(BaseOAuth2):
    name = "linkedin-oauth2"
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    USER_DETAILS_URL = "https://api.linkedin.com/v2/userinfo"
    ACCESS_TOKEN_METHOD = "POST"
    REDIRECT_STATE = False
    DEFAULT_SCOPE = ['openid', 'profile', 'email']
    EXTRA_DATA = [
        ("sub", "uid"),
        ("expires_in", "expires"),
        ("refresh_token", "refresh_token"),
        ("refresh_token_expires_in", "refresh_expires_in"),
    ]

    def user_data(self, access_token, *args, **kwargs):
        """Fetch user data from LinkedIn."""
        response = self.get_json(
            self.USER_DETAILS_URL, headers=self.user_data_headers(access_token)
        )

        # No need to call separate email endpoint if email is already in the /userinfo response
        return response

    def get_user_details(self, response):
        """Return user details from LinkedIn account."""

        fullname = response.get("name", "")
        first_name = response.get("given_name", "")
        last_name = response.get("family_name", "")
        email = response.get("email", "")  # Extract email from /userinfo endpoint
        picture = response.get("picture", "")
        sub = response.get("sub")

        return {
            "username": first_name + last_name,
            "fullname": fullname,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "picture": picture,
            "uid": sub
        }

    def user_data_headers(self, access_token):
        """Prepare headers for user data request."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def request_access_token(self, *args, **kwargs):
        """Request access token from LinkedIn."""
        kwargs["params"] = kwargs.pop("data")
        return super().request_access_token(*args, **kwargs)

    def process_error(self, data):
        """Handle errors during OAuth process."""
        super().process_error(data)
        if data.get("serviceErrorCode"):
            raise AuthCanceled(self, data.get("message") or data.get("status"))


class LinkedinMobileOAuth2(LinkedinOAuth2):
    name = "linkedin-mobile-oauth2"

    def user_data_headers(self, access_token):
        headers = super().user_data_headers(access_token)
        headers["x-li-src"] = "msdk"
        return headers
