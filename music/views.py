from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
from django.contrib.staticfiles import finders
import os
from .utils.lastfm import get_top_artists, get_lastfm_access_token

def top_artists_view(request):
   api_key = 'eade452062ee7a2bd5fcc3c18a888378'
   top_artists = get_top_artists(api_key)
   return render(request, 'your_template.html', {'top_artists': top_artists})


def top_artists():
   lastfm_api_url = "http://ws.audioscrobbler.com/2.0/"

   params = {
      'user': 'Olamideod',
      'api_key': 'eade452062ee7a2bd5fcc3c18a888378',
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
               artists_info.append((name, avatar_url, artist_id))

      return artists_info
   else:
      # Handle the case when the API request is not successful
      return []


# API INTEGRATION FROM LAST.FM
LASTFM_API_KEY = 'eade452062ee7a2bd5fcc3c18a888378'

def get_user_top_artists(request, username):
   # Define the Last.fm API endpoint
   endpoint = 'http://ws.audioscrobbler.com/2.0/?method=user.getTopArtists'

   # Parameters for the API call
   params = {
      'user': username,
      'api_key': LASTFM_API_KEY,
      'period': 'overall',  # You can adjust this based on the desired time period
      'limit': 10,  # Adjust the limit based on your requirements
      'format': 'json',  # You can use 'xml' if you prefer XML format
   }

   # Make the API request
   response = requests.get(endpoint, params=params)
   
   # Check if the request was successful (HTTP status code 200)
   if response.status_code == 200:
      data = response.json()
      top_artists = data.get('topartists', {}).get('artist', [])
      
      # Render the data in your template
      return render(request, 'top_artists.html', {'top_artists': top_artists})
   else:
      # Handle the case where the API request failed
      return render(request, 'error.html', {'error_message': 'Failed to fetch top artists.'})


def css_view(request):
   # Find the path to your style.css file
   css_path = finders.find('style.css')

   # Read the content of the CSS file
   with open(css_path, 'r') as css_file:
      css_content = css_file.read()

   # Create an HttpResponse object and set the content type to 'text/css'
   response = HttpResponse(css_content, content_type='text/css')

   return response

@login_required(login_url="login")
def index(request):
   # Fetch the top artists using the Last.fm API
   api_key = 'eade452062ee7a2bd5fcc3c18a888378'
   top_artists = get_top_artists(api_key)

   # Get the existing artists_info
   artists_info = top_artists()

   context = {
      'artists_info': artists_info,
      'top_artists': top_artists,  # Add the top_artists to the context
   }

   return render(request, 'index.html', context)

def login(request):
   if request.method == 'POST':
      username = request.POST['username'] 
      password = request.POST['password']
      
      user = auth.authenticate(username=username, password=password)
      
      if user is not None:
         auth.login(request, user)
         return redirect('/')
      else:
         messages.info(request, 'Credentials Invalid')
         return redirect('login')
      
   return render(request, 'login.html')

def signup(request):
   if request.method == 'POST':
      email = request.POST['email']
      username = request.POST['username']
      password = request.POST['password']
      password2 = request.POST['password2']

      if password == password2:
         if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')
         elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
         else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # log user in
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            return redirect('/')
      else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
         
   # Render the signup form template for GET requests
   return render(request, 'signup.html')


# Add this function at the end of your views.py file
@login_required(login_url="login")
def lastfm_callback(request):
   # Extract the token and verifier from the Last.fm callback
   token = request.GET.get('token')
   verifier = request.GET.get('oauth_verifier')

   if token and verifier:
      # Use the token and verifier to get the access token from Last.fm
      access_token = get_lastfm_access_token(token, verifier)

      # Store the access token in your user's profile or session as needed
      # This will depend on your authentication and user management setup

      # Redirect or render a success page
      return HttpResponse("Last.fm Authentication Successful!")

   # Handle the case where the token or verifier is missing
   return HttpResponse("Last.fm Authentication Failed. Token or verifier missing.")

@login_required(login_url="login")     
def logout(request):
   auth.logout(request)
   return redirect('login')