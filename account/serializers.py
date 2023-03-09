from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Account

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=['first_name','last_name', 'email','phone_number','password','role']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def create(self, validate_data):
        return Account.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model=Account
        fields = ['email','password','role']

class EmailVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()
