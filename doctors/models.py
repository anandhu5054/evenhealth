from django.db import models
from account.models import Account

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    speciality = models.CharField(max_length=255, blank=True, null=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    license_number = models.CharField(max_length=255, blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    hospital_affiliations = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    publications = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    license_certificate = models.ImageField(upload_to='certificates/', blank=True, null=True)
    certifications_certificate = models.ImageField(upload_to='certificates/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Qualification(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    medical_school = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.PositiveIntegerField()
    study_field = models.CharField(max_length=255, blank=True, null=True)
    medical_school_certificate = models.ImageField(upload_to='certificates/', blank=True, null=True)
    graduation_certificate = models.ImageField(upload_to='certificates/', blank=True, null=True)


class Slot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)