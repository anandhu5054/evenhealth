from django.contrib import admin
from .models import Booking

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'slot', 'created_at', 'paid')
    readonly_fields = ('doctor',)
    
admin.site.register(Booking, BookingAdmin)