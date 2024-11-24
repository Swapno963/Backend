from rest_framework import serializers
from .models import CustomUser, UserProfile, SupplierProfile



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'image', 'address', 'street_address']



class SupplierProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierProfile
        fields = ['id', 'image', 'address', 'street_address', 'license', 'documents']


class CustomUserSerializer(serializers.ModelSerializer):
    
    userprofile = serializers.SerializerMethodField()
    userprofile_update = serializers.JSONField(write_only=True, required=False)  
    
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'phone', 'email', 'userprofile', 'userprofile_update']

        
    def get_userprofile(self, obj):
        if obj.role == 'customer':
            user_profile = UserProfile.objects.filter(user=obj).first()
            if user_profile:
                return UserProfileSerializer(user_profile).data
        elif obj.role == 'supplier':
            supplier_profile = SupplierProfile.objects.filter(user=obj).first()
            if supplier_profile:
                return SupplierProfileSerializer(supplier_profile).data
        return None

    def update(self, instance, validated_data):
        # Update CustomUser fields
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        userprofile_data = validated_data.pop('userprofile_update', None)
        if userprofile_data:
            if instance.role == 'customer':
                profile, created = UserProfile.objects.get_or_create(user=instance)
            elif instance.role == 'supplier':
                profile, created = SupplierProfile.objects.get_or_create(user=instance)
            else:
                profile = None

            if profile:
                for attr, value in userprofile_data.items():
                    setattr(profile, attr, value)
                profile.save()

        return instance



class RegisterSerializer(serializers.ModelSerializer):
    
    confirm_password= serializers.CharField(write_only=True, style={'input_type':'password'})

    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("confirm password doesn't match.")
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user



class LoginSerializer(serializers.Serializer):
    
    phone = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['phone', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }



class ChangePassSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields = ['current_password', 'password', 'confirm_password']
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Confirm password does not match."})
        return data