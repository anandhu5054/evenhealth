from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Account
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor



class DoctorProfileView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor_profile)
        return Response(serializer.data)


    def put(self, request):
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        user = doctor_profile.user
        user_data = request.data.pop('user', {})
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()
        serializer = DoctorProfileSerializer(doctor_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_object_permissions(self, request, obj):
        if request.user.role != 'Doctor':
            raise PermissionDenied