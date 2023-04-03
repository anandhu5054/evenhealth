from rest_framework import generics, filters, status
from .serializers import PatientProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from rest_framework.response import Response
from .permissions import IsPatient
from .models import PatientProfile
from account.models import Account
from .serializers import DoctorDetailSerializer, DoctorListSerializerPatients, PatientProfileUpdateSerializer, PatientSlotSerializer
from doctors.serializers import DoctorProfileSerializer, SlotSerializer
from doctors.models import DoctorProfile, Slot

# Create your views here.

class CreatePatientProfileView(generics.ListCreateAPIView):
    serializer_class = PatientProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsPatient]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveUpdatePateintProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsPatient]

    def get_object(self):
        user = self.request.user
        return PatientProfile.objects.get(user=user)
    
    

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 1


class DoctorListForPatientsAPIView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorListSerializerPatients
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsPatient]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'department__slug']
    ordering_fields = ['user__full_name', 'department__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department', None)

        if department:
            queryset = queryset.filter(department__slug=department)


        queryset = queryset.order_by('user__first_name')

        return queryset

class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAuthenticated,IsPatient]
    authentication_classes = [JWTAuthentication]


class SlotsOfDoctorsAPIView(generics.ListAPIView):
    serializer_class = PatientSlotSerializer
    permission_classes = [IsAuthenticated,IsPatient]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor_id')
        date_str = self.request.query_params.get('date')

        if not doctor_id or not date_str:
            # if doctor_id or date is not present in query parameters, return an empty queryset
            return Slot.objects.none()

        try:
            # parse the date string in format yyyy-mm-dd to a datetime object
            
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # if the date string is not in the correct format, return an empty queryset
            return Slot.objects.none()

        # get the slots for the given doctor and date
        return Slot.objects.filter(doctor_id=doctor_id, date=date, number_of_patients__gt=0)