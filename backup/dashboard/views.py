from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth  # Import the UserSocialAuth model

# Define the DashboardView to render the dashboard template
class DashboardView(LoginRequiredMixin, View):
    login_url = 'http://127.0.0.1:8000/accounts/login/'  # Redirect to the specified login page if not logged in
    redirect_field_name = 'redirect_to'  # Optional: specify the redirect field

    def get(self, request):
        # Initialize the social connections dictionary
        user_social_connections = {
            'linkedin': None,
            'facebook': None,
            'twitter': None,
            'instagram': None,
            'tiktok': None,
        }

        # List of social providers to check
        providers = ['linkedin-oauth2', 'facebook', 'twitter', 'instagram', 'tiktok']

        # Check if the user has linked their social media accounts
        for provider in providers:
            try:
                user_social_auth = request.user.social_auth.get(provider=provider)
                extra_data = user_social_auth.extra_data
                user_social_connections[provider.split('-')[0]] = {
                    'connected': True,
                    'name': f"{extra_data.get('name', '')} ".strip(),
                    'access_token': extra_data.get('access_token', None),
                }
            except UserSocialAuth.DoesNotExist:
                # If the account is not linked, mark as not connected
                user_social_connections[provider.split('-')[0]] = {'connected': False}

        # Prepare the context for the template
        context = {
            'username': request.user.username,  # Pass the username to the template
            'trial_ends_in_days': 6,  # Example value, replace with dynamic logic as needed
            'social_connections': user_social_connections,  # Include social connection status
        }

        # Render the dashboard template
        return render(request, 'dashboard.html', context)

# Define another example view (can be customized as needed)
class SomeOtherView(View):
    def get(self, request):
        context = {
            'message': "This is some other view"
        }
        return render(request, 'other_view.html', context)  # Replace with actual template path
