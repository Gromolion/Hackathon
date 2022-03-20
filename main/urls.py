from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signin/', register, name='signin'),
    path('logout', logout_user, name='logout'),
<<<<<<< HEAD
    path('/<int:pk>/', FolderView.as_view(), name='folder')
]

=======
    path('<int:pk>/', FolderView.as_view(), name='folder')
]
>>>>>>> 3cbcf08b14b49af05a171dd26b87bcf1e752f050
