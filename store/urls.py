from django.urls import path
from .views import CardCreateAPIView,MenuCreateAPIView

urlpatterns = [
    path('cards/create/', CardCreateAPIView.as_view(), name='card-create'),
    path('menus/create/', MenuCreateAPIView.as_view(), name='menu-create'),

]
