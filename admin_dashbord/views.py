from django.db.models import Count, Case, When
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser

class BasicAnalytics(APIView):
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
            "data": analytics
        }, status=status.HTTP_200_OK)
