from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from account.models import Account
from account.serializers import UserRegistrationSerializer
from .models import DoctorProfile, Slot, Department, Qualification
from .serializers import DoctorProfileSerializer, SlotSerializer, QualificationSerializer, DepartmentSerializer
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor, IsApproved


class CreateDoctorProfileview(generics.ListCreateAPIView):
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveUpdateDoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        user = self.request.user
        return DoctorProfile.objects.get(user=user)



class CreateDepartmentView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]
    
    queryset  = Department.objects.all()
    
class CreateQualificationView(generics.ListCreateAPIView):
    serializer_class = QualificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        serializer.save(doctor=doctor)

    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        return Qualification.objects.filter(doctor=doctor)




class SlotListCreateAPIView(generics.ListCreateAPIView):
    """API for doctors to get the slots and create new ones"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
    serializer_class = SlotSerializer

    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        return Slot.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        serializer.save(doctor=doctor)

class SlotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API for the doctors to get, put and delete the slots"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
    serializer_class = SlotSerializer

    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        return Slot.objects.filter(doctor=doctor)

    def perform_destroy(self, instance):
        instance.delete()