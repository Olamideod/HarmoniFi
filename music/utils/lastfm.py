# music/utils/lastfm.py
import requests

def get_top_artists(api_key, limit=10):
    url = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={api_key}&format=json&limit={limit}'
    response = requests.get(url)
    data = response.json()
    return data['artists']['artist']
