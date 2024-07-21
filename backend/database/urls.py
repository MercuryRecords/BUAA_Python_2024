from django.urls import path
from .views import *


urlpatterns = [
    path('user_register', user_register),
    path('message', message),
]