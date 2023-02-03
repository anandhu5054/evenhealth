from django.db import models
from account.models import Account

# Create your models here.

class LaboratoryProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    laboratory_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    number_of_employees = models.PositiveIntegerField(blank=True, null=True)
    license_document = models.FileField(upload_to='laboratory_licenses/', blank=True, null=True)

class LabTest(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    laboratory = models.ForeignKey(LaboratoryProfile, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
