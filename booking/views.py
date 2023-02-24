from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from doctors.models import Slot
from patients.models import PatientProfile
from .serializers import BookingSerializer, ListBookingsPatient
from .models import Booking
from datetime import datetime
from rest_framework.exceptions import ValidationError
from django.utils import timezone
import razorpay
from django.conf import settings
import requests

from patients.permissions import IsPatient, IsApproved, IsVerified


class BookingCreateAPIView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsPatient, IsApproved, IsVerified]

    def create(self, request, *args, **kwargs):
        # Get the slot ID and consultation type from the request data
        slot_id = request.data.get('slot')
        consultation_type = request.data.get('consultation_type')

        try:
            slot = Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            raise ValidationError('Invalid slot ID')

        # Check if the slot is already full
        if slot.number_of_patients <= slot.booked_tokens:
            raise ValidationError('The slot is already full')

        token = slot.booked_tokens

        # Check if the slot start time is in the past
        slot_start_datetime = timezone.make_aware(
            timezone.datetime.combine(slot.date, slot.start_time))
        if slot_start_datetime < timezone.now():
            raise ValidationError('You cannot book a slot that has already started')


        # Create the booking object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(patient=self.request.user.patientprofile, slot=slot, consultation_type=consultation_type,token=token)

        # Create a Razorpay order
        razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        amount = slot.doctor.consultation_fee * 100 # amount in paise
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        }
        order = razorpay_client.order.create(order_data)
        
        booking.order_id = order['id']
        booking.save()

        return Response({
            'booking_id': booking.id,
            'order_id': order['id']
        })


class PaymentVerifyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient, IsApproved, IsVerified]

    def post(self, request, *args, **kwargs):
        # Get the booking ID and payment details from the request data
        booking_id = request.data.get('booking_id')
        payment_id = request.data.get('payment_id')
        payment_signature = request.data.get('payment_signature')

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ValidationError('Invalid booking ID')

        # Verify the payment with Razorpay
        razorpay_client = razorpay.Client(
            auth=(str(settings.RAZORPAY_KEY_ID), str(settings.RAZORPAY_KEY_SECRET)))

        order_id = booking.order_id

        context = {
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": payment_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(context)
        except Exception as e:
            raise ValidationError(str(e))
        
        booking.slot.booked_tokens +=1
        booking.slot.save()
        # Mark the booking as paid and send a confirmation to the user
        booking.paid = True
        booking.save()


        return Response({'status': 'success'})

class ListBookedAppointmentAPI(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ListBookingsPatient
    permission_classes = [IsAuthenticated, IsPatient, IsApproved, IsVerified]

    def get_queryset(self):
        patient = self.request.user.patientprofile
        return Booking.objects.filter(patient=patient, paid=True)
