from django.db import models
from patients.models import PatientProfile
from doctors.models import Slot

# Create your models here.

class Booking(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, related_name='booking',on_delete=models.CASCADE)
    consultation_type = models.CharField(choices=[("online", "Online"), ("offline", "Offline")], max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False) 
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    token = models.IntegerField()  

    def __str__(self):
        return f"{self.patient} - {self.slot.start_time} "

    def doctor(self):
        return self.slot.doctor.user.full_name()
    
    doctor.short_description = 'Doctor'

