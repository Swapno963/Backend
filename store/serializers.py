from rest_framework import serializers
from .models import Card, Menu

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'  



class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  