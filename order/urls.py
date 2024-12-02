from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'card_order', OrderViewSet, basename='order')  
router.register(r'card_payment', PaymentViewSet, basename='payment') 

urlpatterns = router.urls
