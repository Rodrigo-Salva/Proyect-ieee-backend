from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información de Perfil', {'fields': ('role', 'phone', 'biography', 'ieee_id', 'avatar', 'avatar_url', 'avatar_file_id')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'avatar_url']
    list_filter = BaseUserAdmin.list_filter + ('role',)
    readonly_fields = ['avatar_url', 'avatar_file_id']