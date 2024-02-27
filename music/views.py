from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests

def top_artists():
   url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"

   headers = {
      "X-RapidAPI-Key": "14e5d202e1mshb2616e210eec2fdp16681fjsn7931abdea6db",
      "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
   }

   response = requests.get(url, headers=headers)
   response_data = response.json()

   artists_info = []

   # Fix: Correct the variable name to avoid UnboundLocalError
   if 'artists' in response_data:
      for artist in response_data['artists']:
         name = artist.get('name', 'No Name')  # Fix: Change 'artists' to 'artist'
         avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
         artist_id = artist.get('id', 'No ID')
         artists_info.append((name, avatar_url, artist_id))

   return artists_info

@login_required(login_url="login")
def index(request):
   artists_info = top_artists()

   # Fix: Define the context dictionary properly
   context = {
      'artists_info': artists_info
   }
   return render(request, 'index.html', context) # when ever a user is in the index(home page), show the index.html file.


def login(request):
   if request.method == 'POST':
      username = request.POST['username'] 
      password = request.POST['password']
      
      user = auth.authenticate(username=username, password=password)
      
      if user is not None:
         auth.login(request, user)
         return redirect('/')
      else:
         messages.info(request, 'credentials Invalid')
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
            auth.login(request, user_login)  # <-- Fix the typo here
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
