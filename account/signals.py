from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@receiver(post_save, sender=Account)
def create_patient_or_doctor(sender, instance, created, **kwargs):
    print("HELLO")
    if not created:
        print("Haii")
        if instance.role == 'Patient':
            PatientProfile.objects.create(user=instance)
        elif instance.role == 'Doctor':
            DoctorProfile.objects.create(user=instance)
        elif instance.role == 'Doctor':
            PatientProfile.objects.create(user=instance)
