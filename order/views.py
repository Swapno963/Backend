from django.shortcuts import render
from .serializers import OrderSerializer, PaymentSerializer
from .models import Order, Payment

from rest_framework import viewsets, status
from rest_framework.response import Response



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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
