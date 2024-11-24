from django.urls import path, include
from .views import UserProfileView, RegisterUser, LoginUser


urlpatterns = [
     path('user/profile/', UserProfileView.as_view(), name='user_profile'),
     path('user/register/', RegisterUser.as_view(), name='user_register'),
     path('user/login/', LoginUser.as_view(), name='user_login'),
]