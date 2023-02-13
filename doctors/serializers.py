from rest_framework import serializers
from .models import DoctorProfile, Account, Slot, Department, Qualification
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

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('date_of_birth', 'gender', 'address', 'speciality', 'years_experience', 
        'license_number', 'license_expiry_date', 'hospital_affiliations',
        'profile_image', 'experience', 'awards', 'publications', 'languages', 
        'license_certificate', 'certifications_certificate', 'department')


    # def create(self, validated_data):
    #     print("Hello")
    #     request = self.context.get("request")
    #     user = request.user
    #     validated_data['user'] = user
    #     return super().create(validated_data)



class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'date']

    def create(self, validated_data):
        request = self.context.get("request")
        doctor = request.user.doctorprofile
        validated_data['doctor'] = doctor
        return super().create(validated_data)

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        date = data['date']
        request = self.context.get("request")
        doctor = request.user.doctorprofile

        # Check if there is no other slot in the same time and date
        if Slot.objects.filter(start_time__lte=start_time, end_time__gte=end_time, date=date, doctor=doctor).exists():
            raise serializers.ValidationError('There is already a slot in this time and date.')

        return data