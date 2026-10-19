from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Hotel Info', {'fields': ('role', 'phone', 'address', 'profile_picture', 'date_of_birth')}),
        ('Security', {'fields': ('failed_login_attempts', 'lockout_until')}),
    )
