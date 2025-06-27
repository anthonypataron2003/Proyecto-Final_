from django.db import models
from django.urls import reverse
from django.conf import settings

class RecursoEducativo(models.Model):
    CATEGORIA_CHOICES = [
        ('alimentacion', 'Alimentación Saludable'),
        ('monitoreo', 'Monitoreo del Crecimiento'),
        ('recetas', 'Recetas Nutritivas'),
        ('signos', 'Signos de Alerta'),
        ('general', 'General'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    descripcion = models.TextField(verbose_name="Descripción")
    archivo = models.FileField(upload_to='recursos/', verbose_name="Archivo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")
    descargas = models.PositiveIntegerField(default=0, verbose_name="Número de descargas")
    visualizaciones = models.PositiveIntegerField(default=0, verbose_name="Visualizaciones")
    
    class Meta:
        verbose_name = "Recurso Educativo"
        verbose_name_plural = "Recursos Educativos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('detalle_recurso', kwargs={'pk': self.pk})
    
    @property
    def extension_archivo(self):
        if self.archivo:
            return self.archivo.name.split('.')[-1].upper()
        return 'DOC'