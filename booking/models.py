from django.db import models
from patients.models import PatientProfile
from doctors.models import Slot
from django.utils import timezone

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
    refund = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.slot.start_time} "

    def doctor(self):
        return self.slot.doctor.user.full_name()
    
    def is_expired(self):
        expires_at = self.created_at + timezone.timedelta(minutes=5)
        return timezone.now() >= expires_at
    
    doctor.short_description = 'Doctor'


class BlockedSlot(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    blocked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    blocked_token = models.IntegerField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        # expires_at = timezone.now() + timezone.timedelta(minutes=5)
        return timezone.now() >= self.expires_at