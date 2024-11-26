from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from .models import Card, Menu
from .serializers import CardSerializer, MenuSerializer
# Create your views here.
class CardCreateAPIView(APIView):
    def get(self, request, format=None):
        card = [user for user in Card.objects.all()]
        return Response(card)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class MenuCreateAPIView(APIView):
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)