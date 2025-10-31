from django.db import models

from django.conf import settings

class EducationalResource(models.Model):
    """Recursos educativos descargables"""
    
    CATEGORY_CHOICES = (
        ('tutorial', 'Tutorial'),
        ('guide', 'Guía'),
        ('documentation', 'Documentación'),
        ('presentation', 'Presentación'),
        ('other', 'Otro'),
    )
    
    title = models.CharField(max_length=300, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    file = models.FileField(upload_to='resources/', verbose_name='Archivo')
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        verbose_name='Categoría'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='resources',
        verbose_name='Subido Por'
    )
    download_count = models.IntegerField(default=0, verbose_name='Número de Descargas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Recurso Educativo'
        verbose_name_plural = 'Recursos Educativos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
