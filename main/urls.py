from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', login, name='login'),
    path('signin/', register, name='signin'),
    path('logout', logout_user, name='logout'),
    path('<int:pk>/', Home.as_view(), name='folder')
]