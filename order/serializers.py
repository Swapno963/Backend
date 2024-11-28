from rest_framework import serializers
from .models import Order, Payment

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__' 
		# exclude = ['is_paid']

class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['card_code','card','supplier']
		# exclude = ['delivery_date','']


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = '__all__'