from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import ContactForm, SocialLink
from .serializers import ContactFormSerializer, SocialLinkSerializer
from apps.users.permissions import IsAdminUser as CustomIsAdminUser

class ContactFormViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Formularios de Contacto"""
    
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['is_read']
    search_fields = ['full_name', 'email', 'subject']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [CustomIsAdminUser()]
    
    @action(detail=True, methods=['post'], permission_classes=[CustomIsAdminUser])
    def mark_as_read(self, request, pk=None):
        """Marcar formulario como leído"""
        contact = self.get_object()
        contact.is_read = True
        contact.save()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)


class SocialLinkViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Enlaces Sociales"""
    
    queryset = SocialLink.objects.filter(is_active=True).order_by('display_order')
    serializer_class = SocialLinkSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CustomIsAdminUser()]
        return [AllowAny()]