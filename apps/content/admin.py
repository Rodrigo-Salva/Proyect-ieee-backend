from django.contrib import admin
from .models import News, Event, Announcement

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_date', 'image_url']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'image_url', 'image_file_id']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'created_by', 'image_url']
    list_filter = ['event_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_url', 'image_file_id']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'deadline', 'is_active', 'created_by']
    list_filter = ['is_active', 'deadline']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']