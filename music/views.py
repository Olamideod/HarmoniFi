from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
import os

def top_artists():
   lastfm_api_url = "http://ws.audioscrobbler.com/2.0/"

   params = {
      'user': 'your-lastfm-username',
      'api_key': 'your-lastfm-api-key',
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

@login_required(login_url="login")
def index(request):
   artists_info = top_artists()

   context = {
      'artists_info': artists_info
   }
   return render(request, 'index.html', context) # when a user is on the index (home page), show the index.html file.

def lastfm_callback(request):
   # Extract the Last.fm token from the request
   lastfm_token = request.GET.get('token')

   # Your logic to securely handle the Last.fm token (e.g., validate, store, process)

   return HttpResponse("Last.fm callback received successfully!")

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

@login_required(login_url="login")     
def logout(request):
   auth.logout(request)
   return redirect('login')