from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Account, LoginOtp


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model=Account
        fields=['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password', 'role']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validate_data):
        validate_data.pop('confirm_password')
        return Account.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model=Account
        fields = ['email','password','role']


class OtpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='myuser.email', required=True)
    class Meta:
        model = LoginOtp
        fields = ['otp','email']

    def create(self, validated_data):
        myuser_data = validated_data.pop('myuser')
        user = Account.objects.get(email=myuser_data.get("email"))
        loginOtp = LoginOtp.objects.create(myuser=user, **validated_data)
        return loginOtp