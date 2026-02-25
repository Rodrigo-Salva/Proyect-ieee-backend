from rest_framework import serializers
from .models import Chapter, Branch, Member, Position

class PositionSerializer(serializers.ModelSerializer):
    """Serializer para Cargos"""
    
    class Meta:
        model = Position
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MemberSerializer(serializers.ModelSerializer):
    """Serializer para Miembros"""
    
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id', 'full_name', 'email', 'phone', 'position', 'position_name', 
            'chapter', 'chapter_name', 'branch', 'photo', 'photo_url', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_photo_url(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'photo_url') and obj.photo_url:
            return obj.photo_url
            
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class ChapterSerializer(serializers.ModelSerializer):
    """Serializer para Capítulos"""
    
    members_count = serializers.SerializerMethodField()
    members = MemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'icon_url', 'branch', 'members', 'is_active', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()


class MemberDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Miembros"""
    
    chapter = ChapterSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'full_name', 'email', 'phone', 'position', 'chapter', 'branch', 
                 'photo', 'photo_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_photo_url(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'photo_url') and obj.photo_url:
            return obj.photo_url
            
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class BranchSerializer(serializers.ModelSerializer):
    """Serializer para Ramas"""
    
    chapters = ChapterSerializer(many=True, read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'description', 'logo', 'logo_url', 'chapters', 'members', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_logo_url(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'logo_url') and obj.logo_url:
            return obj.logo_url
            
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None