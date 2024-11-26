from django.urls import path
from .views import CardCreateAPIView

urlpatterns = [
    path('cards/create/', CardCreateAPIView.as_view(), name='card-create'),
]
