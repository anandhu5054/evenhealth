from rest_framework import serializers
from .models import PatientProfile
from account.models import Account
from doctors.serializers import DepartmentSerializer, QualificationSerializer
from doctors.models import DoctorProfile
from doctors.validators import RequiredValidator

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = ('user', )

class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', required=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')
    class Meta:
        model = PatientProfile
        exclude = ('user', 'id')

        validators = [
            RequiredValidator(
                fields=(  'date_of_birth', 'gender', 'address',
                    'emergency_contact_name', 'emergency_contact_relationship', 
                    'emergency_contact_phone', 'blood_group', 'height',
                    'weight', 'profile_image'
                )
            )
        ]
    def update(self, instance, validated_data):
        # Extract the doctorfirst_name field from the validated data
        user_data = validated_data.pop('user')
        # Update the instance with the remaining validated data
        instance = super(PatientProfileUpdateSerializer, self).update(instance, validated_data)
        # Update the user's first name if doctorfirst_name is provided
        if user_data:
            instance.user.first_name = user_data.get('first_name')
            instance.user.email = user_data.get('email')
            instance.user.last_name = user_data.get('last_name')
            instance.user.phone_number = user_data.get('phone_number')
            instance.user.save()

        return instance

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
