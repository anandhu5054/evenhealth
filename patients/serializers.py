from rest_framework import serializers
from .models import PatientProfile
from account.models import Account
from doctors.serializers import DepartmentSerializer, QualificationSerializer
from doctors.models import DoctorProfile, Slot
from doctors.validators import RequiredValidator
from account.serializers import AccountDetailSerializer

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)


class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    user = AccountDetailSerializer()
    class Meta:
        model = PatientProfile
        fields = ('user', 'date_of_birth', 'gender',
                  'address', 'blood_group',)

    def update(self, instance, validated_data):
        nested_serializer = self.fields['user']
        nested_instance = instance.user
        nested_data = validated_data.pop('user')
        nested_serializer.update(nested_instance,nested_data)
        return super(PatientProfileUpdateSerializer, self).update(instance, validated_data)

class DoctorSerializerforListing(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['full_name','email']

class DoctorListSerializerPatients(serializers.ModelSerializer):
    user = DoctorSerializerforListing()
    department = DepartmentSerializer()
    class Meta:
        model = DoctorProfile
        fields = ['id','user', 'department','profile_image','address','years_experience']
    
    def get_account(self,obj):
        return DoctorSerializerforListing(obj.account.all(), many=True).data

class DoctorDetailSerializer(serializers.ModelSerializer):
    user = DoctorSerializerforListing()
    qualifications = QualificationSerializer(many=True)
    department = DepartmentSerializer()
    
    class Meta:
        model = DoctorProfile
        fields = ('user', 'date_of_birth', 'gender', 'address', 'years_experience', 
                  'license_number', 
                  'profile_image',
                   'department', 'qualifications')
        

class PatientSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'date']