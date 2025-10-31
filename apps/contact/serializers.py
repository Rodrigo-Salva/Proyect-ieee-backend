from rest_framework import serializers
from .models import ContactForm, SocialLink

class ContactFormSerializer(serializers.ModelSerializer):
    """Serializer para Formularios de Contacto"""
    
    class Meta:
        model = ContactForm
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'submitted_at', 'is_read']
        read_only_fields = ['id', 'submitted_at']


class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer para Enlaces Sociales"""
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url', 'icon_url', 'display_order', 'is_active']
        read_only_fields = ['id']