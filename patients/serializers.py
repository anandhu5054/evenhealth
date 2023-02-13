from rest_framework import serializers
from .models import PatientProfile
from account.models import Account
from doctors.serializers import DepartmentSerializer, QualificationSerializer
from doctors.models import DoctorProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = ('user', )

class DoctorSerializerforListing(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['full_name','email']

class DoctorListSerializerPatients(serializers.ModelSerializer):
    user = DoctorSerializerforListing()
    department = DepartmentSerializer()
    class Meta:
        model = DoctorProfile
        fields = ['user', 'speciality', 'department']
    
    def get_account(self,obj):
        return DoctorSerializerforListing(obj.account.all(), many=True).data

class DoctorDetailSerializer(serializers.ModelSerializer):
    user = DoctorSerializerforListing()
    qualifications = QualificationSerializer(many=True)
    department = DepartmentSerializer()
    
    class Meta:
        model = DoctorProfile
        fields = ('user', 'date_of_birth', 'gender', 'address', 'speciality', 'years_experience', 
                  'license_number', 'license_expiry_date', 'hospital_affiliations',
                  'profile_image', 'experience', 'awards', 'publications', 'languages', 
                   'department', 'qualifications')
