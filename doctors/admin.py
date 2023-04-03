from django.contrib import admin
from .models import DoctorProfile, Slot,Department, Qualification

# Register your models here.


class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'number_of_patients', 'booked_tokens',)
    list_filter = ('doctor', 'date')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name', 'date',)

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'years_experience', 'license_number', 'consultation_fee',)
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'license_number',)
    readonly_fields = ('profile_image', 'license_certificate',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Qualification)