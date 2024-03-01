from django.urls import path
from .views import index, login, signup, logout, lastfm_callback

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('lastfm/callback/', lastfm_callback, name='lastfm_callback'),
]
