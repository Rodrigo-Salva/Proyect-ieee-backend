from django.db import models

class ContactForm(models.Model):
    """Formularios de contacto"""
    
    full_name = models.CharField(max_length=200, verbose_name='Nombre Completo')
    email = models.EmailField(verbose_name='Correo Electrónico')
    subject = models.CharField(max_length=300, verbose_name='Asunto')
    message = models.TextField(verbose_name='Mensaje')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    
    class Meta:
        verbose_name = 'Formulario de Contacto'
        verbose_name_plural = 'Formularios de Contacto'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class SocialLink(models.Model):
    """Enlaces a redes sociales"""
    
    platform = models.CharField(max_length=50, verbose_name='Plataforma')
    url = models.URLField(verbose_name='URL')
    icon_url = models.URLField(blank=True, null=True, verbose_name='URL del Ícono')
    display_order = models.IntegerField(default=0, verbose_name='Orden de Visualización')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Enlace Social'
        verbose_name_plural = 'Enlaces Sociales'
        ordering = ['display_order']
    
    def __str__(self):
        return self.platform
