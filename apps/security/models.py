from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para NutriScan Kids
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Campos adicionales para NutriScan
    specialization = models.CharField(max_length=100, blank=True, help_text="Especialización médica")
    institution = models.CharField(max_length=200, blank=True, help_text="Institución de trabajo")
    license_number = models.CharField(max_length=50, blank=True, help_text="Número de licencia profesional")
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']
    
    class Meta:
        db_table = 'auth_user_custom'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()