from rest_framework import serializers
from .models import News, Event, Announcement

class NewsSerializer(serializers.ModelSerializer):
    """Serializer para Noticias"""
    
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'category', 'author', 'author_email', 'author_username', 
                'published_date', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_image(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'image_url') and obj.image_url:
            return obj.image_url
            
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Noticias"""
    
    author = serializers.StringRelatedField(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_image(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'image_url') and obj.image_url:
            return obj.image_url
            
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class EventSerializer(serializers.ModelSerializer):
    """Serializer para Eventos"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    image = serializers.SerializerMethodField()
    interested_count = serializers.IntegerField(source='interested_users.count', read_only=True)
    is_interested = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_date', 'location', 'image', 
                'registration_link', 'interested_count', 'is_interested', 
                'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_is_interested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.interested_users.filter(id=request.user.id).exists()
        return False

    def get_image(self, obj):
        # Priorizar la URL de ImageKit
        if hasattr(obj, 'image_url') and obj.image_url:
            return obj.image_url
            
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer para Convocatorias"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    days_until_deadline = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'description', 'deadline', 'requirements', 'application_link', 
                'is_active', 'created_by', 'created_by_username', 'days_until_deadline', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_days_until_deadline(self, obj):
        from django.utils import timezone
        delta = obj.deadline - timezone.now()
        return delta.days
