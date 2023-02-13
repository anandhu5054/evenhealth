from django.contrib import admin
from .models import DoctorProfile, Slot,Department, Qualification

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(DoctorProfile)
admin.site.register(Slot)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Qualification)