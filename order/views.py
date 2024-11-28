from django.shortcuts import render
from .serializers import OrderSerializer, PaymentSerializer,OrderCreateSerializer
from .models import Order, Payment

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderSerializer  
        return super().get_serializer_class()


    def create(self, request, *args, **kwargs):
        #custom logic here
        data = request.data.copy()
        data['customer'] = request.user.id  # Associate the order with the logged-in user

        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        # Save the serializer with custom logic 
        serializer.save()
        print("in perform create")

    # Get all order of specific user
    def list(self, request, *args, **kwargs):
        supplier = self.request.query_params.get("supplier")  
        orders = self.queryset.filter(supplier=supplier)  
        serializer = self.get_serializer(orders, many=True)
        return Response({
            "orders": serializer.data
        })
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if editing is allowed
        if instance.is_paid:
            return Response(
                {"error": "This object cannot be edited."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Disable the delete action
        return Response({'error': 'Delete action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Edit action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )


    def destroy(self, request, *args, **kwargs):
        # Disable the delete action
        return Response({'error': 'Delete action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )
