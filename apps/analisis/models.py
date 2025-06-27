# apps/analisis/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class AnalisisNutricional(models.Model):
    """Modelo principal para almacenar el análisis nutricional automático"""
    ESTADO_CHOICES = [
        (0, 'Malnutrido'),
        (1, 'Sobrenutrido'),
        (2, 'Normal'),
        (999, 'Procesando'), 
    ]
    
    SEVERIDAD_CHOICES = [
        ('LEVE', 'Leve'),
        ('MODERADO', 'Moderado'),
        ('SEVERO', 'Severo'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    nombre_paciente = models.CharField(max_length=100, help_text="Nombre del niño/niña")
    edad_meses = models.PositiveIntegerField(help_text="Edad en meses")
    genero = models.CharField(
        max_length=1, 
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        blank=True
    )
    
    imagen = models.ImageField(upload_to='analisis/imagenes/')

    estado_nutricional = models.IntegerField(
        choices=ESTADO_CHOICES, 
        default=999,  
        help_text="Estado nutricional detectado por la IA"
    )
    confianza = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Nivel de confianza del modelo (0.0 - 1.0)",
        default=0.0  
    )
    severidad = models.CharField(
        max_length=10, 
        choices=SEVERIDAD_CHOICES, 
        blank=True, 
        null=True
    )
    
    procesamiento_completado = models.BooleanField(default=False)
    error_procesamiento = models.TextField(blank=True, null=True)
    
    recomendaciones_nutricionales = models.JSONField(
        blank=True,
        null=True,
        help_text="Recomendaciones específicas generadas por el sistema"
    )
    recomendaciones_medicas = models.JSONField(
        blank=True,
        null=True,
        help_text="Recomendaciones médicas según el resultado"
    )
    plan_alimentario = models.TextField(
        blank=True,
        help_text="Plan alimentario sugerido"
    )
    
    fecha_analisis = models.DateTimeField(auto_now_add=True)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    procesado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    observaciones_adicionales = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Análisis Nutricional"
        verbose_name_plural = "Análisis Nutricionales"
        ordering = ['-fecha_analisis']
    
    def __str__(self):
        estado_display = self.get_estado_nutricional_display()
        if self.procesamiento_completado:
            return f"Análisis de {self.nombre_paciente} - {estado_display} ({self.fecha_analisis.strftime('%d/%m/%Y')})"
        else:
            return f"Análisis de {self.nombre_paciente} - En procesamiento ({self.fecha_analisis.strftime('%d/%m/%Y')})"
    
    @property
    def confianza_porcentaje(self):
        """Retorna la confianza en porcentaje"""
        return f"{self.confianza * 100:.1f}%"
    
    @property
    def edad_anos(self):
        """Calcula la edad en años"""
        return self.edad_meses // 12
    
    @property
    def esta_procesando(self):
        """Indica si el análisis está en proceso"""
        return not self.procesamiento_completado and self.estado_nutricional == 999
    
    @property
    def tiene_error(self):
        """Indica si hubo error en el procesamiento"""
        return bool(self.error_procesamiento)
    
    def marcar_procesamiento_completado(self):
        """Marca el análisis como completado"""
        from django.utils import timezone
        self.procesamiento_completado = True
        self.fecha_procesamiento = timezone.now()
        self.save()
    
    def marcar_error_procesamiento(self, error_mensaje):
        """Marca el análisis con error"""
        self.error_procesamiento = error_mensaje
        self.estado_nutricional = 2  # 
        self.confianza = 0.0
        self.save()
    
    def _generar_recomendaciones(self):
        """Genera recomendaciones basadas en el estado nutricional"""
        if not self.procesamiento_completado:
            return {}
            
        recomendaciones = {
            'alimentarias': [],
            'medicas': [],
            'seguimiento': []
        }
        
        if self.estado_nutricional == 0:  
            recomendaciones['alimentarias'] = [
                "Incrementar ingesta calórica con alimentos ricos en nutrientes",
                "Incluir proteínas de alta calidad en cada comida",
                "Agregar grasas saludables como aguacate, frutos secos",
                "Comidas pequeñas y frecuentes (5-6 veces al día)"
            ]
            recomendaciones['medicas'] = [
                "Consulta médica urgente para evaluación completa",
                "Evaluación de posibles deficiencias vitamínicas",
                "Seguimiento mensual del peso y talla"
            ]
            
        elif self.estado_nutricional == 1:  
            recomendaciones['alimentarias'] = [
                "Reducir alimentos procesados y azúcares",
                "Aumentar consumo de frutas y verduras",
                "Controlar porciones de comida",
                "Incrementar actividad física apropiada para la edad"
            ]
            recomendaciones['medicas'] = [
                "Consulta con nutricionista pediátrico",
                "Evaluación de posibles comorbilidades",
                "Seguimiento trimestral del IMC"
            ]
        
        elif self.estado_nutricional == 2: 
            recomendaciones['alimentarias'] = [
                "Mantener dieta balanceada y variada",
                "Continuar con buenos hábitos alimenticios",
                "Asegurar hidratación adecuada",
                "Actividad física regular apropiada para la edad"
            ]
            recomendaciones['medicas'] = [
                "Controles pediátricos regulares",
                "Seguimiento semestral del crecimiento"
            ]
        
        recomendaciones['seguimiento'] = [
            "Registro diario de alimentación",
            "Control de peso semanal",
            "Seguimiento fotográfico mensual"
        ]
        
        return recomendaciones