from rest_framework import serializers
from .models import Menu, Card, ServiceLocation, Favourite

class ServiceLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = ServiceLocation
		fields = ['id', 'address']


class FavouriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favourite
		fields = ['id', 'user', 'card']