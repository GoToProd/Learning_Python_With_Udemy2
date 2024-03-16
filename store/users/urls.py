from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from users.views import login, registration, profile, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]