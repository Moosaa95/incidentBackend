# from rest_framework import serializers
# from .models import CustomUser

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_picture')


from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Incident, Location, Report

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Use the custom User model you've defined
        fields = ('email', 'password', 'first_name', 'surname', 'last_name', 'address', 'type', 'can_login_web')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure the password field is write-only
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            surname=validated_data.get('surname', ''),
            last_name=validated_data.get('last_name', ''),
            address=validated_data['address'],
            type=validated_data.get('type', 'agent'),
            can_login_web=validated_data.get('can_login_web', False),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Include custom claims in the token payload
        user = self.user
        data['email'] = user.email  # Include the email in the token payload

        return data
    

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__' 