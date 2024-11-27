from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceLoactionView, FavouriteView, CardView

router = DefaultRouter()
router.register(r'service-locations', ServiceLoactionView, basename='service_location')
router.register(r'favourite', FavouriteView, basename='favourite')
router.register(r'cards', CardView, basename='cards')

urlpatterns = [
	path('', include(router.urls))	
]
