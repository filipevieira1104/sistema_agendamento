from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_barbeiro', 'whatsapp')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_barbeiro', 'whatsapp')}),
    )