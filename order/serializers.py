from rest_framework import serializers
from .models import Order, Payment

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		# fields = '__all__' 
		exclude = ['customer']


class OrderPartialSerializer(serializers.ModelSerializer):
		class Meta:
			model = Order
			fields = ['delivery_date','sended_by_supplier','status']


class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['card_code','card','supplier']
		# exclude = ['delivery_date','']


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = '__all__'