from django.contrib import admin
from .models import Chapter, Branch, Member, Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_url', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'logo_url', 'logo_file_id']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'chapter', 'is_active', 'photo_url']
    list_filter = ['chapter', 'is_active', 'position']
    search_fields = ['full_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'photo_url', 'photo_file_id']