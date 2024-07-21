from django.urls import path
from .views import *


urlpatterns = [
    path('user_register', user_register),
    path('user_login', user_login),
    path('message', message),
]