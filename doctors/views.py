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
import razorpay
from django.conf import settings


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
            slots = Slot.objects.filter(doctor=doctor, date__range=(start_date, end_date))
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

        booked_slots = Booking.objects.filter(slot=instance,canceled=False,paid=True,refund=False)
        
        for booked_slot in booked_slots:
            razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            try:
                refund_amount = booked_slot.slot.doctor.consultation_fee * 100
                refund = razorpay_client.payment.refund(instance.payment_id, {'amount': refund_amount})
            except:
                # TODO: handle the exception
                pass
            booked_slot.slot.number_of_patients +=1
            booked_slot.slot.save()
            booked_slot.refund = True
            booked_slot.canceled = True
            booked_slot.save()

        return Response({'status': 'success'})

class BookedAppointmentsAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor, IsApproved]
    serializer_class = BookedAppointmentsSerializer
    
    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.get(user=user)
        slot = Slot.objects.filter(doctor=doctor)

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
            slot = Slot.objects.filter(doctor=doctor, date=date)
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            slot = Slot.objects.filter(doctor=doctor, date__range=(start_date, end_date))
        if past_slots:
            slot = Slot.objects.filter(doctor=doctor, date__lt=today)
        elif future_slots:
            slot = Slot.objects.filter(doctor=doctor, date__gte=today)
           

        return Booking.objects.filter(slot__in=slot,paid=True)