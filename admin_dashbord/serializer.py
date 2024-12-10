from rest_framework import serializers
from accounts.models import CustomUser
from django.db.models import Count, Sum
from store.models import ServiceLocation
class LocationAnalyticsSerializer(serializers.ModelSerializer):
    num_orders = serializers.IntegerField()

    class Meta:
        model = ServiceLocation
        # fields = ['num_orders','num_card']
        fields = '__all__'
