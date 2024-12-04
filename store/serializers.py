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


class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = ['menu_id', 'name', 'description', 'image']



class CardSerializer(serializers.ModelSerializer):
	menu = MenuSerializer(many=True, source='menus')

	class Meta:
		model = Card
		fields = ['id', 'card_id', 'title', 'price', 'duration', 'service_location', 'is_active', 'is_feature', 'description', 'menu']

