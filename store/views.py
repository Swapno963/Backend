from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from .serializers import ServiceLocationSerializer, FavouriteSerializer
from .models import Menu, Card, ServiceLocation, Favourite
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class ServiceLoactionView(viewsets.ViewSet):
	serializer_class = ServiceLocationSerializer
	
	def get_queryset(self):
		return ServiceLocation.objects.all()

	@extend_schema(
		description = 'get all service locations list',
		responses={200:ServiceLocationSerializer(many=True)}
		)
	def list(self, request):
		queryset = self.get_queryset()
		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)



class FavouriteView(viewsets.ModelViewSet):
	serializer_class = FavouriteSerializer
	permission_classes = [IsAuthenticated]
	http_method_names = ['get', 'post', 'delete']
	
	def get_queryset(self):
		return Favourite.objects.filter(user=self.request.user)

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	

