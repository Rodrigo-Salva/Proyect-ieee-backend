from django.contrib import admin
from .models import EducationalResource

@admin.register(EducationalResource)
class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_by', 'download_count']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'download_count']