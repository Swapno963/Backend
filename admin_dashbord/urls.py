from django.urls import path
from .views import BasicAnalyticsOfUsers,BasicAnalyticsOfOrder,BasicAnalyticsOfStore
urlpatterns = [
    path('user_basic/', BasicAnalyticsOfUsers.as_view()),
    path('order_basic/', BasicAnalyticsOfOrder.as_view()),
    path('stor_basic/', BasicAnalyticsOfStore.as_view()),
]




