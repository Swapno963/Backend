from django.urls import path, include
from .views import UserProfileView, RegisterUser, LoginUser, ChangePassword, LogoutUser


urlpatterns = [
     path('user/profile/', UserProfileView.as_view(), name='user_profile'),
     path('user/register/', RegisterUser.as_view(), name='register'),
     path('user/login/', LoginUser.as_view(), name='login'),
     path('user/logout/', LogoutUser.as_view(), name='logout'),
     path('user/change-password/', ChangePassword.as_view(), name='change_password'),
]