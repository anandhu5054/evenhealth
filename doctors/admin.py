from django.contrib import admin
from .models import DoctorProfile, Slot

# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(Slot)