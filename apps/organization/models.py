from django.db import models

class Chapter(models.Model):
    """Capítulos técnicos de IEEE"""
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    icon_url = models.URLField(blank=True, null=True, verbose_name='URL del Ícono')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Capítulo'
        verbose_name_plural = 'Capítulos'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    """Ramas estudiantiles de IEEE"""
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    logo = models.ImageField(upload_to='branches/', blank=True, null=True, verbose_name='Logo')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Rama'
        verbose_name_plural = 'Ramas'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Member(models.Model):
    """Miembros del equipo"""
    
    full_name = models.CharField(max_length=200, verbose_name='Nombre Completo')
    email = models.EmailField(verbose_name='Correo Electrónico')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    position = models.CharField(max_length=100, verbose_name='Cargo')
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='members',
        verbose_name='Capítulo'
    )
    photo = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name='Foto')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.position}"
