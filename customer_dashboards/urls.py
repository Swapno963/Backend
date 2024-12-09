from django.urls import path, include
from .views import CustomerDashboardView


urlpatterns = [
	path('client_dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
]