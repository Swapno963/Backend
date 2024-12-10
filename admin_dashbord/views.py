from django.db.models import Count, Case, When
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
from order.models import Order
from store.models import ServiceLocation


class BasicAnalyticsOfUsers(APIView):
    """
    Showing different types of analytics
    like: total users, total customers, and total suppliers.
    """
    queryset = CustomUser.objects.all() 

    def get(self, request, format=None):
        """
        Return a list of analytics.
        """
        # Count total users, customers, and suppliers
        analytics = CustomUser.objects.aggregate(
            total_users=Count('id'),
            total_admins=Count(Case(When(role='super_admin', then=1))),
            total_customers=Count(Case(When(role='customer', then=1))),
            total_suppliers=Count(Case(When(role='supplier', then=1))),
        )

        return Response({
            "data": analytics,
        }, status=status.HTTP_200_OK)


class BasicAnalyticsOfOrder(APIView):
    """
    Showing total order, order status
    """
    queryset = Order.objects.all() 

    def get(self, request, format=None):
        """
        Return a list of analytics.
        """
        # Count total users, customers, and suppliers
        analytics = Order.objects.aggregate(
            #showing  total oder object
            total_order=Count('id'),

            # showing status of order
            pending_status=Count(Case(When(status=Order.PENDING, then=1))),
            accepted_status=Count(Case(When(status=Order.ACCEPTED, then=1))),
            delevered_status=Count(Case(When(status=Order.DELIVERED, then=1))),

            # Showing how many order is paid is true
            paid_count=Count(Case(When(is_paid=True, then=1))),
            unpaid_count=Count(Case(When(is_paid=False, then=1))),
        )

        return Response({
            "data": analytics
        }, status=status.HTTP_200_OK)



class BasicAnalyticsOfStore(APIView):
    """
    Showing all our location we have
    
    """
    queryset = CustomUser.objects.all() 

    def get(self, request, format=None):
        """
        Return a list of location.
        """
      
        service_location = ServiceLocation.objects.values('id', 'address')
        return Response({
            "Service location":list(service_location),
        }, status=status.HTTP_200_OK)
