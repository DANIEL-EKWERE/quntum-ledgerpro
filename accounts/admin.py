from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_verified', 'two_factor_enabled', 'created_at']
    list_filter = ['is_verified', 'two_factor_enabled', 'is_staff']
    search_fields = ['email', 'username']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('phone', 'country', 'avatar', 'referral_code', 'referred_by')}),
        ('Security', {'fields': ('two_factor_enabled', 'two_factor_secret', 'is_verified')}),
    )
