from django.db import models
from django.conf import settings
import os
from config.imagekit_client import upload_image_to_imagekit, delete_image_from_imagekit

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
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='URL de ImageKit')
    image_file_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de archivo ImageKit')
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

    def save(self, *args, **kwargs):
        is_new_image = False
        if not self.pk:
            if self.image:
                is_new_image = True
        else:
            old_instance = News.objects.filter(pk=self.pk).first()
            if old_instance:
                old_image_name = old_instance.image.name if old_instance.image else None
                new_image_name = self.image.name if self.image else None
                if new_image_name and old_image_name != new_image_name:
                    is_new_image = True

        super().save(*args, **kwargs)

        if is_new_image and self.image:
            try:
                if old_instance and old_instance.image_file_id:
                    delete_image_from_imagekit(old_instance.image_file_id)

                with self.image.open('rb') as f:
                    file_data = f.read()
                    response = upload_image_to_imagekit(
                        file_content=file_data,
                        file_name=os.path.basename(self.image.name),
                        folder="news/"
                    )
                    
                    if hasattr(response, 'url') and response.url:
                        self.image_url = response.url
                        self.image_file_id = response.file_id
                        News.objects.filter(pk=self.pk).update(
                            image_url=self.image_url,
                            image_file_id=self.image_file_id
                        )
            except Exception as e:
                print(f"Error subiendo imagen de noticia a ImageKit: {e}")

    def delete(self, *args, **kwargs):
        if self.image_file_id:
            delete_image_from_imagekit(self.image_file_id)
        super().delete(*args, **kwargs)


class Event(models.Model):
    
    title = models.CharField(max_length=300, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    event_date = models.DateTimeField(verbose_name='Fecha del Evento')
    location = models.CharField(max_length=300, verbose_name='Ubicación')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Imagen')
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='URL de ImageKit')
    image_file_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de archivo ImageKit')
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

    def save(self, *args, **kwargs):
        is_new_image = False
        if not self.pk:
            if self.image:
                is_new_image = True
        else:
            old_instance = Event.objects.filter(pk=self.pk).first()
            if old_instance:
                old_image_name = old_instance.image.name if old_instance.image else None
                new_image_name = self.image.name if self.image else None
                if new_image_name and old_image_name != new_image_name:
                    is_new_image = True

        super().save(*args, **kwargs)

        if is_new_image and self.image:
            try:
                if old_instance and old_instance.image_file_id:
                    delete_image_from_imagekit(old_instance.image_file_id)

                with self.image.open('rb') as f:
                    file_data = f.read()
                    response = upload_image_to_imagekit(
                        file_content=file_data,
                        file_name=os.path.basename(self.image.name),
                        folder="events/"
                    )
                    
                    if hasattr(response, 'url') and response.url:
                        self.image_url = response.url
                        self.image_file_id = response.file_id
                        Event.objects.filter(pk=self.pk).update(
                            image_url=self.image_url,
                            image_file_id=self.image_file_id
                        )
            except Exception as e:
                print(f"Error subiendo imagen de evento a ImageKit: {e}")

    def delete(self, *args, **kwargs):
        if self.image_file_id:
            delete_image_from_imagekit(self.image_file_id)
        super().delete(*args, **kwargs)


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
