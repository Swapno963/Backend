from .serializers import OrderSerializer, PaymentSerializer,OrderCreateSerializer
from .models import Order, Payment
from rest_framework.decorators import action

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['customer'] = request.user.id 
        serializer = self.OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
    

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Delete action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        #custom logic here
        data = request.data.copy()
        data['customer'] = request.user.id
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Edit action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )


    def destroy(self, request, *args, **kwargs):
        # Disable the delete action
        return Response({'error': 'Delete action is not allowed.'}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED                        )
