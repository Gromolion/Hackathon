from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', login, name='login'),
    path('signin/', RegisterUser.as_view(), name='signin'),
    path('profile', profile, name='profile')
]