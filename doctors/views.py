from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from account.models import Account
from account.serializers import UserRegistrationSerializer
from .models import DoctorProfile, Slot, Department, Qualification
from adminpanel.serializers import DoctorDetailSerializer, AccountSerializerForLisiting
from .serializers import DoctorProfileSerializer, CreateDoctorProfileSerializer, BookedAppointmentsSerializer, SlotSerializer, QualificationSerializer, DepartmentSerializer
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsDoctor, IsApproved
from datetime import datetime
from django.db import IntegrityError
from booking.models import Booking



class CreateDoctorProfileview(generics.ListCreateAPIView):
    serializer_class = CreateDoctorProfileSerializer
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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:            
            self.perform_update(serializer)
        except IntegrityError as e:
            error_msg = str(e)
            if 'email' in error_msg:
                error_data = {'email': ['An account with this email already exists.']}
            elif 'phone_number' in error_msg:
                error_data = {'phone_number': ['An account with this phone number already exists.']}
            else:
                error_data = {'detail': ['An error occurred while updating the profile.']}

            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

class CreateDepartmentView(generics.ListCreateAPIView):
    """Creating a new department and to list all departments"""
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]
    
    queryset  = Department.objects.all()


class RetrieveDepartmentView(generics.RetrieveAPIView):
    """Retrieving a single department"""
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()

    
class CreateQualificationView(generics.ListCreateAPIView):
    """API for creating qualification of doctors"""
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
        # Getting date from url(query_params)
        date_str = self.request.query_params.get('date')
        if date_str:
            #Getting Slots of a particular date
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return Slot.objects.filter(doctor=doctor, date=date)
        else:
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

class BookedAppointmentsAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
    serializer_class = BookedAppointmentsSerializer
    
    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        slot = Slot.objects.filter(doctor=doctor)
        return Booking.objects.filter(slot__in=slot,paid=True)