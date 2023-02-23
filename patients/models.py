from django.db import models
from account.models import Account


# Create your models here.
class PatientProfile(models.Model):
    user = models.OneToOneField(Account, related_name="patientprofile" ,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('AB+', 'AB+ve'),
        ('O+', 'O+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('AB-', 'AB-ve'),
        ('O-', 'O-ve'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.full_name()