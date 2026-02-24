from django.db import models
from django.conf import settings

class News(models.Model):
    """Noticias y actualizaciones"""
    
    CATEGORY_CHOICES = (
        ('announcement', 'Comunicado'),
        ('event', 'Evento'),
        ('achievement', 'Logro'),
        ('general', 'General'),
    )

    title = models.CharField(max_length=300, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Imagen')
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='general',
        verbose_name='Categoría'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='news',
        verbose_name='Autor'
    )
    published_date = models.DateTimeField(verbose_name='Fecha de Publicación')
    is_published = models.BooleanField(default=False, verbose_name='Publicado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    
    title = models.CharField(max_length=300, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    event_date = models.DateTimeField(verbose_name='Fecha del Evento')
    location = models.CharField(max_length=300, verbose_name='Ubicación')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Imagen')
    registration_link = models.URLField(blank=True, null=True, verbose_name='Link de Registro')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='events_created',
        verbose_name='Creado Por'
    )
    interested_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='interested_events',
        verbose_name='Usuarios Interesados'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-event_date']
    
    def __str__(self):
        return self.title


class Announcement(models.Model):
    """Convocatorias y llamados"""
    
    title = models.CharField(max_length=300, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    deadline = models.DateTimeField(verbose_name='Fecha Límite')
    requirements = models.TextField(verbose_name='Requisitos')
    application_link = models.URLField(blank=True, null=True, verbose_name='Link de Postulación')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='announcements',
        verbose_name='Creado Por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Convocatoria'
        verbose_name_plural = 'Convocatorias'
        ordering = ['-deadline']
    
    def __str__(self):
        return self.title
