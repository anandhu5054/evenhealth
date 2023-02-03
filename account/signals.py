from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from labs.models import LaboratoryProfile

@receiver(post_save, sender=Account)
def create_patient_or_doctor(sender, instance, created, **kwargs):
    if not created:
        if instance.role == 'Patient':
            PatientProfile.objects.get_or_create(user=instance)
        elif instance.role == 'Doctor':
            DoctorProfile.objects.get_or_create(user=instance)
        elif instance.role == 'Lab':
            LaboratoryProfile.objects.get_or_create(user=instance)
