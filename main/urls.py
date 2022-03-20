from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signin/', register, name='signin'),
    path('logout', logout_user, name='logout'),
    path('/<int:pk>/', FolderView.as_view(), name='folder')
]