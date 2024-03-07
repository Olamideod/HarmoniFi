# music/utils/lastfm.py
import requests
import hashlib  # Import hashlib module for generating MD5 hash
import json

def get_top_artists(api_key):
    lastfm_api_url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        'user': 'Olamideod',  # Replace with the desired Last.fm username
        'api_key': api_key,
        'format': 'json'
    }

    response = requests.get(lastfm_api_url + 'user/top/artists', params=params)

    if response.status_code == 200:
        response_data = response.json()
        artists_info = []

        if 'topartists' in response_data:
            for artist in response_data['topartists']['artist']:
                name = artist.get('name', 'No Name')
                avatar_url = artist.get('image', [{}])[-1].get('#text', 'No URL')
                artist_id = artist.get('mbid', 'No ID')

                # Create a dictionary for each artist
                artist_dict = {
                    'name': name,
                    'image': avatar_url,
                    'id': artist_id,
                }

                artists_info.append(artist_dict)

        return artists_info
    else:
        # Handle the case when the API request is not successful
        return []


LASTFM_API_KEY = 'eade452062ee7a2bd5fcc3c18a888378'
LASTFM_API_SECRET = 'f2451esswtEmy42mb9nPG6tcpKQQijsDV5Wq9'
LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0/'

def get_lastfm_access_token(temporary_token, verifier):
    # Parameters for the API call to obtain the access token
    params = {
        'method': 'auth.getSession',
        'api_key': LASTFM_API_KEY,
        'token': temporary_token,
        'api_sig': generate_api_signature(temporary_token, verifier),
        'format': 'json',
    }

    # Make the API request
    response = requests.get(LASTFM_API_URL, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get('session', {}).get('key')

        if access_token:
            return access_token

    # Handle the case where the API request failed or access token is not available
    raise Exception("Failed to obtain Last.fm access token")

def generate_api_signature(token, verifier):
    # Generate the API signature using the Last.fm API secret
    api_signature = f'api_key{LASTFM_API_KEY}methodauth.getSessiontoken{token}verifier{verifier}{LASTFM_API_SECRET}'
    return hashlib.md5(api_signature.encode('utf-8')).hexdigest()



def lastfm_get(payload):
    # Define headers and URL
    headers = {'user-agent': 'Dataquest'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = 'your_lastfm_api_key'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # Create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)