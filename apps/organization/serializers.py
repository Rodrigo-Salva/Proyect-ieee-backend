from rest_framework import serializers
from .models import Chapter, Branch, Member

class ChapterSerializer(serializers.ModelSerializer):
    """Serializer para Capítulos"""
    
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'icon_url', 'is_active', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()


class BranchSerializer(serializers.ModelSerializer):
    """Serializer para Ramas"""
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'description', 'logo', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MemberSerializer(serializers.ModelSerializer):
    """Serializer para Miembros"""
    
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    
    class Meta:
        model = Member
        fields = ['id', 'full_name', 'email', 'phone', 'position', 'chapter', 'chapter_name', 
                  'photo', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MemberDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Miembros"""
    
    chapter = ChapterSerializer(read_only=True)
    
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']