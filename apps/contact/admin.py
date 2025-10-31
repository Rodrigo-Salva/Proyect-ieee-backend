from django.contrib import admin
from .models import ContactForm, SocialLink

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['full_name', 'email', 'subject']
    readonly_fields = ['submitted_at', 'full_name', 'email', 'subject', 'message']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'display_order', 'is_active']
    list_filter = ['is_active', 'platform']
    search_fields = ['platform']