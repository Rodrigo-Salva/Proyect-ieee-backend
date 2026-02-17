from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

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
    http_method_names = ['get', 'post', 'head'] # Restrict to read-only + creation

    def perform_create(self, serializer):
        instance = serializer.save()
        
        try:
            subject = f"Nuevo mensaje de contacto: {instance.subject}"
            message = f"""
            Has recibido un nuevo mensaje de contacto:
            
            Nombre: {instance.full_name}
            Email: {instance.email}
            Asunto: {instance.subject}
            
            Mensaje:
            {instance.message}
            """
            
            admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ieeetecsup.com',
                [admin_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
    
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