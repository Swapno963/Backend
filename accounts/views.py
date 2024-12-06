from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile, CustomUser, SupplierProfile, BlacklistedToken
from drf_spectacular.utils import extend_schema
from django.contrib import auth
from rest_framework.decorators import action
from rest_framework_simplejwt.exceptions import InvalidToken
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


    @action(detail=False, methods=['post'], url_path=r'update/')
    @extend_schema(
        request=CustomUserSerializer,
        responses={
            200: CustomUserSerializer,
            400: 'Invalid request',
        },
        description='Update user profile information'
    )
    def patch(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



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
                return Response({'errors':'your login credentials are not valid'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.headers.get('Refresh')

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"detail": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = request.headers.get("Authorization", None)
        if access_token:
            try:
                parts = access_token.split()
                if len(parts) == 2 and parts[0].lower() == "bearer":
                    token = parts[1]
                    BlacklistedToken.objects.create(token=token)
                else:
                    return Response({"detail": "Invalid access token format"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"Invalid access token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)




class ChangePassword(APIView):
    serializer_class = ChangePassSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
                current_password = request.data.get('current_password')
                password = request.data.get('password')

                if not user.check_password(current_password):
                        return Response({'errors':'Current password does not match.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(password)
                user.save()
                return Response({'messages':'password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



