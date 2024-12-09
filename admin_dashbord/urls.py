from django.urls import path
from .views import BasicAnalytics
urlpatterns = [
    path('admin_basic/', BasicAnalytics.as_view()),
]



