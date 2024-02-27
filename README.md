
HarmoniFi: Last.fm Integration Testing on Vercel
Introduction:

This document guides you through setting up and testing the Last.fm API integration for your HarmoniFi music application using Vercel for temporary deployment.

Prerequisites:

A Vercel account (https://vercel.com/)
A Last.fm developer account (https://www.last.fm/api)
A Django project for your HarmoniFi application
Steps:

1. Secure Callback URL:

Create a secure route: Within your Django app, create a URL pattern and a corresponding view function to handle the Last.fm callback securely. Here's an example:
Python
from django.urls import path

def lastfm_callback(request):
    # Extract the Last.fm token from the request
    lastfm_token = request.GET.get('token')

    # Your logic to securely handle the Last.fm token (e.g., validate, store, process)

    return HttpResponse("Last.fm callback received successfully!")

urlpatterns = [
    path('lastfm/callback/', lastfm_callback, name='lastfm_callback'),
]
Use code with caution.
Obtain the public URL: Once deployed to Vercel, the path after your Vercel domain will be your secure callback URL. For example, if your Vercel domain is "your-app-name.vercel.app", the callback URL would be:
https://your-app-name.vercel.app/lastfm/callback/
2. Register App with Last.fm:

Visit the Last.fm API developer page: https://www.last.fm/api
Create a developer account and register your app.
Important: During registration, under "Website", enter a placeholder website URL for your testing purposes (e.g., "http://localhost:8000").
Use the secure callback URL obtained from Vercel as the "Callback URL" during registration.
3. Deploy to Vercel:

Follow Vercel's documentation for Django deployment: https://vercel.com/templates/python/django-hello-world
Push your code with the secure callback URL implementation to a dedicated testing branch in your Git repository.
Deploy the testing branch to Vercel.
4. Testing:

Use the Vercel public URL (e.g., "[invalid URL removed]") to access your deployed application for testing.
Utilize the Last.fm API features within your HarmoniFi app to trigger the callback functionality.
Verify that the Last.fm callback is received successfully by your secure route on Vercel, indicating successful integration (refer to your server logs or implement logging mechanisms within your view function).
Important Notes:

Security: Always prioritize secure token handling practices within your view function. Avoid logging sensitive information like tokens in plain text.
Environment Variables: Store sensitive information like API keys in environment variables and not directly in the code or URL.
Temporary Setup: Remember, this setup is solely for testing purposes and should not be used in production due to limitations of Vercel. Consider a more robust platform like Zeet for production deployment.
Additional Tips:

Utilize a clear branching strategy in your Git repository to differentiate between development, testing, and production code.
Consider using environment variables or a configuration file to manage different configurations (e.g., API keys) for testing and production environments.
Thoroughly test your Last.fm integration functionalities within your HarmoniFi app on Vercel before transitioning to production deployment.
