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
from datetime import date
from django.utils import timezone


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



# class SlotListAPIView(generics.ListAPIView):
#     """API for doctors to get the slots"""
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
#     serializer_class = SlotSerializer
#     filter_backends = [filters.OrderingFilter, filters.DateFromToRangeFilter]
#     ordering_fields = ['date', 'start_time']
#     date_fields = ['date']

#     def get_queryset(self):
#         user = self.request.user
#         doctor = DoctorProfile.objects.get(user=user)

#         queryset = Slot.objects.filter(doctor=doctor)

#         # Filter for past or future slots
#         slot_filter = self.request.query_params.get('slot_filter', None)
#         if slot_filter == 'past':
#             queryset = queryset.filter(date__lt=timezone.now().date())
#         elif slot_filter == 'future':
#             queryset = queryset.filter(date__gte=timezone.now().date())

#         # Filter for date range or specific date
#         date_from = self.request.query_params.get('date_from', None)
#         date_to = self.request.query_params.get('date_to', None)
#         date = self.request.query_params.get('date', None)

#         if date_from and date_to:
#             queryset = queryset.filter(date__range=[date_from, date_to])
#         elif date:
#             queryset = queryset.filter(date=date)

#         return queryset


class SlotListCreateAPIView(generics.ListCreateAPIView):
    """API for doctors to get the slots and create new ones"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
    serializer_class = SlotSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)

        date_str = self.request.query_params.get('date')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')
        past_slots = self.request.query_params.get('past_slots')
        future_slots = self.request.query_params.get('future_slots')

        from datetime import date
        today = date.today()

        if date_str:
            #Getting Slots of a particular date
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return Slot.objects.filter(doctor=doctor, date=date)
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            slots = Slot.objects.filter(doctor=doctor, date__range=(start_date, end_date), date__lt=date.today())
            return slots

        if past_slots:
            queryset = Slot.objects.filter(doctor=doctor, date__lt=today)
            return queryset
        elif future_slots:
            queryset = Slot.objects.filter(doctor=doctor, date__gte=today)
            return queryset        

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