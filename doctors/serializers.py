from rest_framework import serializers
from .models import DoctorProfile, Account, Slot

class DoctorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')

    class Meta:
        model = DoctorProfile
        fields = (
            'first_name', 'last_name','email', 'phone_number',
            'date_of_birth', 'gender', 'address', 'speciality', 
            'years_experience', 'medical_school', 'graduation_year', 
            'license_number', 'license_expiry_date', 'certifications', 
            'hospital_affiliations', 'profile_image', 'bio', 'education', 
            'experience', 'awards', 'publications', 'languages', 'medical_school_certificate',
            'graduation_certificate', 'license_certificate', 'certifications_certificate'
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')
        phone_number = user_data.get('phone_number')

        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.email = email
        instance.user.phone_number = phone_number
        instance.user.save()

        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.years_experience = validated_data.get('years_experience', instance.years_experience)
        instance.medical_school = validated_data.get('medical_school', instance.medical_school)
        instance.graduation_year = validated_data.get('graduation_year', instance.graduation_year)
        instance.license_number = validated_data.get('license_number', instance.license_number)
        instance.license_expiry_date = validated_data.get('license_expiry_date', instance.license_expiry_date)
        instance.certifications = validated_data.get('certifications', instance.certifications)
        instance.hospital_affiliations = validated_data.get('hospital_affiliations', instance.hospital_affiliations)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.education = validated_data.get('education', instance.education)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.awards = validated_data.get('awards', instance.awards)
        instance.publications = validated_data.get('publications', instance.publications)
        instance.languages = validated_data.get('languages', instance.languages)
        instance.medical_school_certificate = validated_data.get('medical_school_certificate', instance.medical_school_certificate)
        instance.graduation_certificate = validated_data.get('graduation_certificate', instance.graduation_certificate)
        instance.license_certificate = validated_data.get('license_certificate', instance.license_certificate)
        instance.certifications_certificate = validated_data.get('certifications_certificate', instance.certifications_certificate)
        instance.save()
        return instance

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