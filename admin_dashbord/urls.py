from django.urls import path
from .views import BasicAnalyticsOfUsers,BasicAnalyticsOfOrder
urlpatterns = [
    path('user_basic/', BasicAnalyticsOfUsers.as_view()),
    path('order_basic/', BasicAnalyticsOfOrder.as_view()),
]



