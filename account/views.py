from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserRegistrationSerializer,LoginSerializer,EmailVerificationSerializer
from django.contrib.auth import  authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tasks import send_email_task
from django.conf import settings
from account.models import Account

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
        email = request.data.get('email')
        if Account.objects.filter(email=email,is_verified=False).exists():
            pass

        if serializer.is_valid(raise_exception=True):            
            user= serializer.save()
            user.save()
            otp = random.randint(100000, 999999)
            subject = "Email Verification OTP"
            message = f"Your OTP is {otp}"
            recipient_list = user.email
            from_email=settings.EMAIL_HOST_USER
            send_email_task.apply_async(args=[subject, message, from_email,[recipient_list]])
            request.session['otp'] = otp
            return Response({'msg':'Please check the mail for the OTP'},status=status.HTTP_201_CREATED)
        
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
                return Response({'msg':'Username OR Password does not match'})


class EmailVerificationAPI(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        otp = random.randint(100000, 999999)
        subject = "Email Verification OTP"
        message = f"Your OTP is {otp}"
        recipient_list = user.email
        from_email=settings.EMAIL_HOST_USER
        # send_mail(subject, message, from_email,[recipient_list])
        send_email_task.apply_async(args=[subject, message, from_email,[recipient_list]])
        request.session['otp'] = otp
        return Response({"message": "OTP sent to email successfully."}, status=status.HTTP_200_OK)

class EmailVerificationOTPAPI(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = int(serializer.validated_data.get("otp"))
        if otp and otp == request.session.get('otp'):
            user.is_verified = True
            user.save()
            request.session.pop('otp')
            return Response({"message": "Email Verified Successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)