from rest_framework import serializers

from account.models import Account
from doctors.models import DoctorProfile
from doctors.serializers import DoctorProfileSerializer, QualificationSerializer, DepartmentSerializer



class AdminDoctorApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['is_approved']
        

"""The below two serializers are used to list doctors to admin with some details"""
class AccountSerializerForLisiting(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name','is_approved','email','phone_number','is_verified']
        extra_kwargs = {
            'email': {'validators': []},
            'phone_number':{'validators': []},
        }
    
    # def update(self,instance,validated_data):
    #     instance.email=validated_data.get('email', instance.email)
    #     instance.phone_number=validated_data.get('email', instance.phone_number)
    #     instance.save()
    #     return instance

class DoctorListSerializer(serializers.ModelSerializer):
    user = AccountSerializerForLisiting()
    department = DepartmentSerializer()
    class Meta:
        model = DoctorProfile
        fields = ['user', 'speciality', 'department']
    
    def get_account(self,obj):
        return AccountSerializerForLisiting(obj.account.all(), many=True).data

class DoctorDetailSerializer(serializers.ModelSerializer):
    user = AccountSerializerForLisiting()
    qualifications = QualificationSerializer(many=True)
    department = DepartmentSerializer()
    
    class Meta:
        model = DoctorProfile
        fields = ('user', 'date_of_birth', 'gender', 'address', 'speciality', 'years_experience', 
                  'license_number', 'license_expiry_date', 'hospital_affiliations',
                  'profile_image', 'experience', 'awards', 'publications', 'languages', 
                  'license_certificate', 'certifications_certificate', 'department', 'qualifications')
    
    def update(self, instance, validated_data):
        # breakpoint()
        user_data = validated_data.pop('user', None)
        # breakpoint()
        if user_data:
            account_serializer = self.fields['user']
            account_instance = account_serializer.update(instance.user, user_data)
            instance.user = account_instance
            # instance.user.save()
        breakpoint()
        address_serializer = self.fields['address']
        address_instance = address_serializer.update(instance.address, validated_data)
        instance.address = address_instance
        # breakpoint()
        instance.save()
        return instance