from django.db import models
from account.models import Account


# Create your models here.
class PatientProfile(models.Model):
    user = models.OneToOneField(Account, related_name="patientprofile" ,on_delete=models.CASCADE)  ###
    profile_image = models.ImageField(upload_to='profile_images/')  ###
    date_of_birth = models.DateField()  ###
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES) #
    address = models.CharField(max_length=255)  ###
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
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)

    def __str__(self):
        return self.user.full_name()