from django.urls import path
from .views import BookingCreateAPIView, PaymentVerifyAPIView

urlpatterns = [
    path('create_booking_doctor', BookingCreateAPIView.as_view(), name='booking_create'),
    path('verifypayment',PaymentVerifyAPIView.as_view(),name='payment_verification')
]