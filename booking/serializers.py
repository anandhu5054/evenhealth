from rest_framework import serializers
from .models import Booking
from patients.models import PatientProfile

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['slot', 'consultation_type']

    def create(self,validated_data):
        request = self.context.get("request")
        patient = PatientProfile.objects.get(user=request.user)
        validated_data['patient'] = patient
        return super().create(validated_data)

class ListBookingsPatient(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['slot', 'consultation_type','token']