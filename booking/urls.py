from django.urls import path
from .views import BookingCreateAPIView, PaymentVerifyAPIView, ListBookedAppointmentAPI

urlpatterns = [
    path('create_booking_doctor', BookingCreateAPIView.as_view(), name='booking_create'),
    path('verifypayment',PaymentVerifyAPIView.as_view(),name='payment_verification'),
    path('booked',ListBookedAppointmentAPI.as_view(),name='booked')
]