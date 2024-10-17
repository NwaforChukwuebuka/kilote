from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from .models import SocialMediaAccount
from django.utils.decorators import method_decorator
import requests
from social_django.models import UserSocialAuth
from django.contrib import messages
import tweepy
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import tweepy
from django.conf import settings
from requests_oauthlib import OAuth1Session

def save_twitter_token(user, token):
    """Save Twitter access token for the user."""
    try:
        user_social_auth = user.social_auth.get(provider='twitter')
        user_social_auth.extra_data['access_token'] = token
        user_social_auth.save()  # Save the user social auth object with the new token
    except UserSocialAuth.DoesNotExist:
        # Handle the case where the user does not have a Twitter account linked
        pass

@login_required
def linkedin_post(request):
    if request.method == "POST":
        message = request.POST.get('message')
        print(message)
        
        if not message:
            # Handle empty message error by redirecting with an error message
            return render(request, 'dashboard.html', {'error': 'Message cannot be empty'})

        # Here, we assume the user has linked their LinkedIn account
        try:
            user_social_auth = request.user.social_auth.get(provider='linkedin-oauth2')
            access_token = user_social_auth.extra_data['access_token']
            uid = user_social_auth.extra_data['uid']  # Ensure uid is available
        except UserSocialAuth.DoesNotExist:
            # Handle case where the user hasn't linked their LinkedIn account
            return render(request, 'dashboard.html', {'error': 'LinkedIn account not linked'})

        # Check if the uid is valid
        if not uid:
            return render(request, 'dashboard.html', {'error': 'LinkedIn account is not properly linked. Please reconnect.'})

        # LinkedIn API endpoint for creating a post
        post_url = 'https://api.linkedin.com/v2/ugcPosts'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
        }

        # Create the post body as per LinkedIn's API requirements
        post_data = {
            "author": f"urn:li:person:{uid}",  # Format the author field correctly
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": message  # Use the provided message
                    },
                    "shareMediaCategory": "NONE"  # Set to NONE for text-only post
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"  # Set visibility to public
            }
        }

        # Send the post request to LinkedIn
        response = requests.post(post_url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            # Successful post creation
            messages.success(request, 'Post successfully created on LinkedIn!')
            return redirect('dashboard')  # Redirect to the dashboard or desired page
        else:
            # Handle LinkedIn API errors
            error_message = response.json().get('message', 'Unknown error occurred')
            return render(request, 'dashboard.html', {'error': f'Unable to post to LinkedIn: {error_message}'})

    return render(request, 'dashboard.html')


@login_required
def unlink_social_account(request, platform):
    try:
        # Get the user social auth object for the specified platform
        social_account = request.user.social_auth.get(provider=platform)

        # Remove the social account
        social_account.delete()

        messages.success(request, f"{platform.title()} account successfully unlinked.")
    except UserSocialAuth.DoesNotExist:
        messages.error(request, f"No linked account found for {platform.title()}.")

    return redirect('/dashboard')  # Replace with your actual dashboard URL


@login_required
def linkedin_complete(request):
    """
    This view handles the LinkedIn OAuth process completion.
    """
    return redirect('dashboard')  # Redirect to the desired page after completion


    

@login_required
def twitter_connect(request):
    auth = tweepy.OAuth1UserHandler(
        settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, 
        settings.SOCIAL_AUTH_TWITTER_REDIRECT_URI
    )
    try:
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepError:
        return redirect('error_page')

@login_required
def twitter_callback(request):
    # Retrieve the request token from the session
    request_token = request.session.pop('request_token', None)

    # Initialize the OAuth1 handler
    auth = tweepy.OAuth1UserHandler(
        settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET
    )

    # Get the verifier from the callback URL
    verifier = request.GET.get('oauth_verifier')

    # Set the request token in the OAuth handler
    auth.request_token = {
        'oauth_token': request_token['oauth_token'],
        'oauth_token_secret': request_token['oauth_token_secret']
    }
    
    try:
        # Get the access token using the verifier
        auth.get_access_token(verifier)

        # Now that we have access tokens, we can create an API object
        api = tweepy.API(auth)

        # Fetch the authenticated user's details
        twitter_user = api.verify_credentials()

        # Extract the required user details
        twitter_profile_image_url = twitter_user.profile_image_url_https  # User's profile image URL
        screen_name = twitter_user.screen_name  # User's Twitter handle
        access_token = auth.access_token  # OAuth access token
        access_token_secret = auth.access_token_secret  # OAuth access token secret

        # Save or update the social media account in the database
        SocialMediaAccount.objects.update_or_create(
            user=request.user,  # Ensure the user is logged in
            platform_name='Twitter',
            defaults={
                'profile_image': twitter_profile_image_url,
                'full_name': screen_name,  # Make sure screen_name is fetched here
                'access_token': access_token,
                'access_token_secret': access_token_secret,
            }
        )

        # Redirect to dashboard or wherever you'd like after success
        return redirect('dashboard')

    except tweepy.TweepError as e:
        # Log the error for debugging
        print(f"Error during Twitter authentication: {e}")
        return redirect('error_page')

@login_required
def post_to_twitter_view(request):
    if request.method == 'POST':
        # Get the tweet message from the form
        tweet_text = request.POST.get('message')

        # Get the user's Twitter account from the database
        try:
            twitter_account = SocialMediaAccount.objects.get(user=request.user, platform_name='Twitter')
        except SocialMediaAccount.DoesNotExist:
            return redirect('error_page')  # Handle error if Twitter account isn't found

        # Retrieve the necessary credentials
        consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
        consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET
        access_token = twitter_account.access_token
        access_token_secret = twitter_account.access_token_secret

        # Post the tweet
        try:
            post_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text)
            return redirect('dashboard')  # Redirect to dashboard after success
        except Exception as e:
            return redirect('error_page')  # Handle any errors

    return redirect('dashboard')

def post_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text):
    """
    Post a tweet to Twitter using OAuth1.

    Parameters:
    - consumer_key: Twitter API consumer key (from settings)
    - consumer_secret: Twitter API consumer secret (from settings)
    - access_token: OAuth access token (from SocialMediaAccount)
    - access_token_secret: OAuth access token secret (from SocialMediaAccount)
    - tweet_text: The content of the tweet (from the form)

    Returns:
    - response: Twitter API response
    """
    
    # Create OAuth1 session
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Twitter API v2 endpoint for posting tweets
    tweet_url = "https://api.twitter.com/2/tweets"
    
    # Payload for the tweet content
    payload = {"text": tweet_text}

    # Send the request
    response = oauth.post(tweet_url, json=payload)

    # Check if the response is successful
    if response.status_code == 201:
        print("Tweet posted successfully!")
    else:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    
    return response