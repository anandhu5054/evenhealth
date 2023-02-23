from django.contrib import admin
from .models import PatientProfile

# Register your models here.

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'blood_group', 'height', 'weight')
    list_filter = ('gender', 'blood_group')

admin.site.register(PatientProfile, PatientProfileAdmin)