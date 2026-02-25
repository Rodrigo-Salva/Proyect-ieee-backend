from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from config.imagekit_client import upload_image_to_imagekit, delete_image_from_imagekit
import os

class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User"""
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """Modelo de usuario personalizado con roles"""
    
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('public', 'Público'),
    )
    
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='public',
        verbose_name='Rol'
    )
    
    # Profile fields
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    biography = models.TextField(blank=True, null=True, verbose_name='Biografía')
    ieee_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='IEEE ID')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    avatar_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='URL de ImageKit')
    avatar_file_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ImageKit File ID')
    interested_chapters = models.ManyToManyField(
        'organization.Chapter', 
        blank=True, 
        related_name='interested_users',
        verbose_name='Capítulos de Interés'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        is_new_avatar = False
        old_avatar_name = None
        old_file_id = None

        if self.pk:
            try:
                old_instance = User.objects.get(pk=self.pk)
                old_avatar_name = old_instance.avatar.name if old_instance.avatar else None
                old_file_id = old_instance.avatar_file_id
                
                # Detect change or removal
                new_avatar_name = self.avatar.name if self.avatar else None
                if old_avatar_name and old_avatar_name != new_avatar_name:
                    # Clean up old file from local storage
                    print(f"Borrando avatar antiguo local: {old_avatar_name}")
                    try:
                        old_instance.avatar.storage.delete(old_avatar_name)
                    except Exception as e:
                        print(f"Error borrando archivo local: {e}")
                    
                    # Clean up from ImageKit
                    if old_file_id:
                        print(f"Borrando avatar antiguo de ImageKit: {old_file_id}")
                        from config.imagekit_client import delete_image_from_imagekit
                        delete_image_from_imagekit(old_file_id)
                        self.avatar_file_id = None
                        self.avatar_url = None

                if new_avatar_name and old_avatar_name != new_avatar_name:
                    is_new_avatar = True
            except User.DoesNotExist:
                pass
        else:
            if self.avatar:
                is_new_avatar = True

        super().save(*args, **kwargs)

        # Upload new avatar to ImageKit
        if is_new_avatar and self.avatar:
            try:
                from config.imagekit_client import upload_image_to_imagekit
                print(f"Subiendo nuevo avatar a ImageKit: {self.avatar.name}")
                with self.avatar.open('rb') as f:
                    file_data = f.read()
                    response = upload_image_to_imagekit(
                        file_content=file_data,
                        file_name=os.path.basename(self.avatar.name),
                        folder="avatars/"
                    )
                    
                    if hasattr(response, 'url') and response.url:
                        self.avatar_url = response.url
                        self.avatar_file_id = getattr(response, 'file_id', None)
                        # Actualizar sin disparar save() de nuevo
                        User.objects.filter(pk=self.pk).update(
                            avatar_url=self.avatar_url,
                            avatar_file_id=self.avatar_file_id
                        )
            except Exception as e:
                print(f"Error subiendo a ImageKit: {e}")

    def delete(self, *args, **kwargs):
        # Borrar el avatar de ImageKit antes de eliminar el usuario
        if self.avatar_file_id:
            print(f"Eliminando avatar de ImageKit por borrado de usuario: {self.avatar_file_id}")
            delete_image_from_imagekit(self.avatar_file_id)
        super().delete(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_public(self):
        return self.role == 'public'
