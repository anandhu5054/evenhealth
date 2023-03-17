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
    doctorName = serializers.CharField(source='slot.doctor.user.full_name')
    start_time = serializers.CharField(source='slot.start_time')
    end_time = serializers.CharField(source='slot.end_time')
    date = serializers.CharField(source='slot.date')
    department = serializers.CharField(source='slot.doctor.department.name')
    class Meta:
        model = Booking
        fields = ['id','doctorName','department','start_time','end_time','date', 'consultation_type','token']

class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['slot', 'consultation_type']