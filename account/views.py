from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer,LoginSerializer
from django.contrib.auth import  authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            user= serializer.save()
            user.save()
            return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)

class RegisterDoctortView(APIView):
    def post(self, request, format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            user= serializer.save()
            user.role = "Doctor"
            user.save()
            return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)

class RegisterLabView(APIView):
    def post(self, request, format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            user= serializer.save()
            user.role = "Lab"
            user.save()
            return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)

class UserLogin(APIView):
    def post(self, request , format=None):
        serializer= LoginSerializer(data= request.data)
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user:
                token= get_tokens_for_user(user)
                return Response({'token':token , 'msg':'Login Successful'})

            else:
                return Response({'msg':'Login Failed'})