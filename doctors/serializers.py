from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .validators import RequiredValidator
from datetime import datetime
from django.db.models import Q

from .models import DoctorProfile, Account, Slot, Department, Qualification
from booking.models import Booking
from account.serializers import UserRegistrationSerializer



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

 
class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        exclude = ('doctor', )
    
    def create(self, validated_data):
        request = self.context.get("request")
        doctor = request.user.doctorprofile
        validated_data['doctor'] = doctor
        return super().create(validated_data)
    

class CreateDoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)


class DoctorProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', required=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')
    class Meta:
        model = DoctorProfile
        fields = ('email', 'first_name','last_name', 'phone_number', 'date_of_birth', 'gender', 'address', 'speciality', 'years_experience', 
        'license_number', 'license_expiry_date', 'hospital_affiliations',
        'profile_image', 'experience', 'awards', 'publications', 'languages', 
        'license_certificate', 'certifications_certificate', 'department')
             
        validators = [
            RequiredValidator(
                fields=(  'date_of_birth', 'gender', 'address', 'speciality', 'years_experience', 
        'license_number', 'license_expiry_date', 'hospital_affiliations',
        'profile_image', 'experience', 'awards', 'publications', 'languages', 
        'license_certificate', 'certifications_certificate', 'department')
            )
        ]

    def update(self, instance, validated_data):
        # Extract the doctorfirst_name field from the validated data
        user_data = validated_data.pop('user')
        # Update the instance with the remaining validated data
        instance = super(DoctorProfileSerializer, self).update(instance, validated_data)
        # Update the user's first name if doctorfirst_name is provided
        if user_data:
            instance.user.first_name = user_data.get('first_name')
            instance.user.email = user_data.get('email')
            instance.user.last_name = user_data.get('last_name')
            instance.user.phone_number = user_data.get('phone_number')
            instance.user.save()

        return instance


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'date','number_of_patients']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        doctor = DoctorProfile.objects.get(user=user)
        validated_data['doctor'] = doctor
        return super().create(validated_data)

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        date = data['date']
        request = self.context.get("request")
        user = request.user
        doctor = DoctorProfile.objects.get(user=user)
        start_datetime = datetime.combine(date, start_time)
        start_datetime = start_datetime.replace(tzinfo=timezone.utc)

        # Check if there is no other slot in the same time and date
        if Slot.objects.filter(
            Q(start_time__lt=end_time, end_time__gt=start_time) |  # overlaps partially or completely with existing slot
            Q(start_time__lte=start_time, end_time__gte=end_time),  # completely overlaps with existing slot
            date=date,
            doctor=doctor
        ).exists():
            raise serializers.ValidationError('There is already a slot in this time and date.')
        elif start_datetime <= timezone.now() + timedelta(hours=2):
            raise serializers.ValidationError('You can only add slots with start times that are at least two hours from now ')
        return data


class BookedAppointmentsSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(source='patient.user.full_name')
    start_time = serializers.CharField(source='slot.start_time')
    end_time = serializers.CharField(source='slot.end_time')
    date = serializers.CharField(source='slot.date')
    class Meta:
        model = Booking
        fields = ['patientName','start_time','end_time','date', 'consultation_type','token']