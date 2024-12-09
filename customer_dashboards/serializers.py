from rest_framework import serializers
from accounts.models import CustomUser, UserProfile
from order.models import Order, Payment
from accounts.serializers import CustomUserSerializer
from order.serializers import OrderSerializer, PaymentSerializer



class CurrentPlanSerializer(serializers.Serializer):
	current_card = serializers.CharField(max_length=250)
	duration = serializers.IntegerField()


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image', 'address', 'street_address']


class CustomerSerializer(serializers.ModelSerializer):
    userprofile = CustomerProfileSerializer(read_only=True)  
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'userprofile']



class CustomerDashboardSerializer(serializers.Serializer):
	
	customer_info = CustomerSerializer()
	current_plan = CurrentPlanSerializer(allow_null=True)
	orders = OrderSerializer(many=True, allow_null=True)
	payments = PaymentSerializer(many=True, allow_null=True)
	total_expense = serializers.CharField(allow_null=True)

