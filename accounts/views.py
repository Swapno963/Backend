from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer, CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile, CustomUser, SupplierProfile
from drf_spectacular.utils import extend_schema
from django.contrib import auth
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class RegisterUser(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    @extend_schema(
        description="Register a user.",
        request=RegisterSerializer
    )
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'message':'Registration success'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    @extend_schema(
        responses={
            200: CustomUserSerializer,
        },
        request=CustomUserSerializer,
        description='Retrieve user profile or update profile information'
    )

    def get(self, request, *args, **kwargs):
        user = request.user
        user_serializer = CustomUserSerializer(user)
    
        response_data = {
            'profile': user_serializer.data,
        }      
        return Response(response_data, status=status.HTTP_200_OK)
    



class RegisterUser(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    @extend_schema(
        description="Register a user.",
        request=RegisterSerializer
    )
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'Registration success'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginUser(APIView):
    
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="User login area",
        request=LoginSerializer
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            phone = request.data.get('phone')
            password = request.data.get('password')
            user = auth.authenticate(phone=phone, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                user_serializer = CustomUserSerializer(user)
                return Response({'token':token, 'user':user_serializer.data, 'message':'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':'phone and password is not valid'}, status=status/HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
