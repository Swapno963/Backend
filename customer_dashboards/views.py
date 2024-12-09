from django.shortcuts import render
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.permissions import  IsAuthenticated
from order.models import Order, Payment
from store.models import Card
from order.serializers import OrderSerializer, PaymentSerializer
from .serializers import CustomerDashboardSerializer, CustomerSerializer
from accounts.serializers import CustomUserSerializer
# Create your views here.


class CustomerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(customer__user=user.id)
        current_order = orders.filter(is_paid=True).first()
        current_plan = None
        if current_order:
            current_card = current_order.card_code  
            card = Card.objects.filter(card_id=current_card).first() 
            duration = card.duration if card else 0
            current_plan = {
                'current_card': current_card,
                'duration': duration,
            }

        total_expense = Payment.objects.filter(customer__user=user.id, is_confirmed=True).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        payments = Payment.objects.filter(customer__user=user.id)
        user_serializer = CustomUserSerializer(user)  
        order_serializer = OrderSerializer(orders, many=True)  
        payment_serializer = PaymentSerializer(payments, many=True)
        data = {
            'customer_info': user_serializer.data,
            'current_plan': current_plan,
            'orders': order_serializer.data,
            'payments': payment_serializer.data,
            'total_expense': total_expense,
        }

        serializer = CustomerDashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
