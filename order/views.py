from .serializers import OrderSerializer, PaymentSerializer,OrderCreateSerializer,OrderPartialSerializer
from .models import Order, Payment
from rest_framework.decorators import action

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderSerializer  
        elif self.action =="partial_update":
            return OrderPartialSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['customer'] = request.user.id 
        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()

    # Get all order of specific user
    def list(self, request, *args, **kwargs):
        supplier = self.request.query_params.get("supplier")  
        orders = self.queryset.filter(supplier=supplier)  
        serializer = self.get_serializer(orders, many=True)
        return Response({
            "orders": serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        allowed_fields = {"delivery_date", "sended_by_supplier", "status"}
        for field in request.data.keys():
            if field not in allowed_fields:
                raise ValidationError({field: "This field cannot be updated."})
        return super().partial_update(request, *args, **kwargs)
    
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
        data['customer'] = request.user.id  # Associate the payment with the logged-in user
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
