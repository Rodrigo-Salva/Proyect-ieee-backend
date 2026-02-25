from django.db import models
import os
from config.imagekit_client import upload_image_to_imagekit, delete_image_from_imagekit

class Position(models.Model):
    """Cargos o roles dentro de la organización"""
    
    name = models.CharField(max_length=100, verbose_name='Nombre del Cargo')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Chapter(models.Model):
    """Capítulos técnicos de IEEE"""
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    icon_url = models.URLField(blank=True, null=True, verbose_name='URL del Ícono')
    branch = models.ForeignKey(
        'Branch',
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='Rama',
        null=True,
        blank=True
    )
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
    logo_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='URL de Logo ImageKit')
    logo_file_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de logo ImageKit')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Rama'
        verbose_name_plural = 'Ramas'
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new_logo = False
        if not self.pk:
            if self.logo:
                is_new_logo = True
        else:
            old_instance = Branch.objects.filter(pk=self.pk).first()
            if old_instance:
                old_logo_name = old_instance.logo.name if old_instance.logo else None
                new_logo_name = self.logo.name if self.logo else None
                if new_logo_name and old_logo_name != new_logo_name:
                    is_new_logo = True

        super().save(*args, **kwargs)

        if is_new_logo and self.logo:
            try:
                if old_instance and old_instance.logo_file_id:
                    delete_image_from_imagekit(old_instance.logo_file_id)

                with self.logo.open('rb') as f:
                    file_data = f.read()
                    response = upload_image_to_imagekit(
                        file_content=file_data,
                        file_name=os.path.basename(self.logo.name),
                        folder="branches/"
                    )
                    
                    if hasattr(response, 'url') and response.url:
                        self.logo_url = response.url
                        self.logo_file_id = response.file_id
                        Branch.objects.filter(pk=self.pk).update(
                            logo_url=self.logo_url,
                            logo_file_id=self.logo_file_id
                        )
            except Exception as e:
                print(f"Error subiendo logo de rama a ImageKit: {e}")

    def delete(self, *args, **kwargs):
        if self.logo_file_id:
            delete_image_from_imagekit(self.logo_file_id)
        super().delete(*args, **kwargs)


class Member(models.Model):
    """Miembros del equipo"""
    
    full_name = models.CharField(max_length=200, verbose_name='Nombre Completo')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name='Cargo'
    )
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='members',
        verbose_name='Capítulo'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name='Rama (Directa)'
    )
    photo = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name='Foto')
    photo_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='URL de Foto ImageKit')
    photo_file_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de foto ImageKit')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.position.name if self.position else 'Sin cargo'}"

    def save(self, *args, **kwargs):
        is_new_photo = False
        if not self.pk:
            if self.photo:
                is_new_photo = True
        else:
            old_instance = Member.objects.filter(pk=self.pk).first()
            if old_instance:
                old_photo_name = old_instance.photo.name if old_instance.photo else None
                new_photo_name = self.photo.name if self.photo else None
                if new_photo_name and old_photo_name != new_photo_name:
                    is_new_photo = True

        super().save(*args, **kwargs)

        if is_new_photo and self.photo:
            try:
                if old_instance and old_instance.photo_file_id:
                    delete_image_from_imagekit(old_instance.photo_file_id)

                with self.photo.open('rb') as f:
                    file_data = f.read()
                    response = upload_image_to_imagekit(
                        file_content=file_data,
                        file_name=os.path.basename(self.photo.name),
                        folder="members/"
                    )
                    
                    if hasattr(response, 'url') and response.url:
                        self.photo_url = response.url
                        self.photo_file_id = response.file_id
                        Member.objects.filter(pk=self.pk).update(
                            photo_url=self.photo_url,
                            photo_file_id=self.photo_file_id
                        )
            except Exception as e:
                print(f"Error subiendo foto de miembro a ImageKit: {e}")

    def delete(self, *args, **kwargs):
        if self.photo_file_id:
            delete_image_from_imagekit(self.photo_file_id)
        super().delete(*args, **kwargs)
