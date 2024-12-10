from django.db.models import Count, Case, When,Avg,Min,Max,Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
from order.models import Order,Payment
from store.models import ServiceLocation


from .serializer import LocationAnalyticsSerializer

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

        # first and last added user 
        first_join_users = CustomUser.objects.all().order_by('-joined_date')
        users = {f"{user.name}": user.joined_date for user in first_join_users}

        return Response({
            "data": analytics,
            "first_join_users":users,
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

        # Taking about money
        payment_analisis = Payment.objects.all().aggregate(
            min_order=Min('total_amount'),
            max_order=Max('total_amount'),
            avg_order=Avg('total_amount'),
            total_order=Sum('total_amount'),
            
            # Showing how many order is paid is true
            confirmed=Count(Case(When(is_confirmed=True, then=1))),
            unconfirmed=Count(Case(When(is_confirmed=False, then=1))),
            )


        # Taking about payment method
        payment_methos = Payment.objects.values('payment_method') \
                        .annotate(count=Count('payment_method')) \
                        .order_by('-count')
        
        return Response({
            "data": analytics,
            "payment_analisis":payment_analisis,
            "payment_methos":payment_methos,
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
        
        service_locations_orders = ServiceLocation.objects.annotate(
            num_orders=Count("address"),
            num_card=Count("card"),
            )
        serializer = LocationAnalyticsSerializer(service_locations_orders, many=True)


        num_orders_per_customer = CustomUser.objects.annotate(
            num_orders=Count('order')).values(
                'id','name', 'num_orders'
                ).order_by('-num_orders')
        
        num_payments_per_customer = CustomUser.objects.annotate(
            num_payments=Count('payment')).values(
                'id','name', 'num_payments'
                ).order_by("-num_payments")
        
        customer_orders = {f"{user['name']}": user['num_orders'] for user in num_orders_per_customer}
        customer_payments = {f"{user['name']}": user['num_payments'] for user in num_payments_per_customer}

        return Response({
            "Service location":list(service_location),
            "service_locations_orders":serializer.data,
            "customer_orders":customer_orders,
            "customer_payments":customer_payments,
        }, status=status.HTTP_200_OK)
