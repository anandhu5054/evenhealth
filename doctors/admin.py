from django.contrib import admin
from .models import DoctorProfile, Slot,Department, Qualification

# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(Slot)
admin.site.register(Department)
admin.site.register(Qualification)