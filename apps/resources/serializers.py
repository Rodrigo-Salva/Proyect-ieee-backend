from rest_framework import serializers
from .models import EducationalResource

class EducationalResourceSerializer(serializers.ModelSerializer):
    """Serializer para Recursos Educativos"""
    
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = EducationalResource
        fields = ['id', 'title', 'description', 'file', 'file_url', 'category', 'chapter', 'chapter_name',
                'uploaded_by', 'uploaded_by_username', 'download_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uploaded_by', 'download_count', 'created_at', 'updated_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
