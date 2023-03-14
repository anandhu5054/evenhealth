from django.contrib import admin
from .models import Account, LoginOtp
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        
        "last_login",
        "date_joined",
        "is_active",
    )
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name','phone_number', 'username','password1', 'password2'),
    }),
)

admin.site.register(Account,AccountAdmin)
admin.site.register(LoginOtp)