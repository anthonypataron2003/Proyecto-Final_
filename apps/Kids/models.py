from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.analisis.models import AnalisisNutricional



class HistorialMedico(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    analisis = models.ForeignKey(AnalisisNutricional, on_delete=models.CASCADE)
    notas = models.TextField(blank=True)
    fecha_seguimiento = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Historial de {self.usuario.username} - {self.analisis.fecha}"