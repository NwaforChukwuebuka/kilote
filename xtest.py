from requests_oauthlib import OAuth1Session
import os
import json

# Your Twitter API credentials
consumer_key = '8Vy7zJGSC3SFa5Rn71wR5daC5'
consumer_secret = '0pFEnOPDqxHg1mYOLHjhoa7BBFhNFRxeTHIMC6kYf7KrU9dLRP'
access_token = '1667534077832855552-sBv9UhU7WSfDvjgK5RaNrl4tPr2GX2'
access_token_secret = '5JS4zuvaMuMsZDRA8Uk8noR7O90q13UJupDvgfpDpBTDv'

# OAuth1 session
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Correct Twitter API v2 endpoint
tweet_url = "https://api.twitter.com/2/tweets"

# Correct payload format for Twitter API v2
payload = {"text": "Second APi Test!"}

# Send the request
response = oauth.post(tweet_url, json=payload)

# Check if the response is successful
if response.status_code != 201:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

print("Tweet posted successfully!")
