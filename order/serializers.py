from rest_framework import serializers
from .models import Order, Payment

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		exclude = ['customer']


class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['card_code','card']

class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = '__all__'