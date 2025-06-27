# apps/analisis/forms/AnalisisForm.py
from django import forms
from django.core.validators import FileExtensionValidator
from apps.analisis.models import AnalisisNutricional

class AnalisisNutricionalForm(forms.ModelForm):
    """Formulario para crear y editar análisis nutricionales"""
    
    class Meta:
        model = AnalisisNutricional
        fields = [
            'nombre_paciente',
            'edad_meses', 
            'genero',
            'imagen',
            'observaciones_adicionales'
        ]
        
        widgets = {
            'nombre_paciente': forms.TextInput(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20 hover:border-primary/40 bg-white/70',
                'placeholder': 'Ej: María García',
                'id': 'nombre_paciente'
            }),
            'edad_meses': forms.NumberInput(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent/50 transition-all duration-300 border border-primary/20 hover:border-accent/40 bg-white/70',
                'placeholder': 'Ej: 36',
                'min': '0',
                'max': '216',
                'id': 'edad_meses'
            }),
            'genero': forms.Select(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-300 border border-primary/20 hover:border-secondary/40 bg-white/70',
                'id': 'genero'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'absolute inset-0 w-full h-full opacity-0 cursor-pointer',
                'accept': 'image/*',
                'id': 'imagen'
            }),
            'observaciones_adicionales': forms.Textarea(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-warning/50 transition-all duration-300 border border-primary/20 hover:border-warning/40 resize-none bg-white/70',
                'placeholder': 'Información adicional sobre el estado de salud, alergias, etc.',
                'rows': '3',
                'id': 'observaciones_adicionales'
            })
        }
        
        labels = {
            'nombre_paciente': '',
            'edad_meses': '',
            'genero': '',
            'imagen': '',
            'observaciones_adicionales': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Validaciones personalizadas
        self.fields['imagen'].validators = [
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp'],
                message='Solo se permiten archivos JPG, PNG y WEBP'
            )
        ]
        
        # Configurar campos requeridos
        self.fields['nombre_paciente'].required = True
        self.fields['edad_meses'].required = True
        self.fields['genero'].required = True
        self.fields['imagen'].required = True
        self.fields['observaciones_adicionales'].required = False
        
        # Help texts personalizados
        self.fields['nombre_paciente'].help_text = 'Nombre completo del niño o niña'
        self.fields['edad_meses'].help_text = 'Edad en meses (0-216 meses = 0-18 años)'
        self.fields['genero'].help_text = 'Seleccionar el género del paciente'
        self.fields['imagen'].help_text = 'Imagen clara del niño/niña. Máximo 10MB'
        self.fields['observaciones_adicionales'].help_text = 'Información adicional relevante (opcional)'

    def clean_nombre_paciente(self):
        """Validar nombre del paciente"""
        nombre = self.cleaned_data.get('nombre_paciente', '').strip()
        
        if len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres')
        
        if len(nombre) > 100:
            raise forms.ValidationError('El nombre no puede exceder 100 caracteres')
            
        # Validar que contenga solo letras, espacios y caracteres acentuados
        import re
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        
        return nombre

    def clean_edad_meses(self):
        """Validar edad en meses"""
        edad = self.cleaned_data.get('edad_meses')
        
        if edad is None:
            raise forms.ValidationError('La edad es requerida')
        
        if edad < 0:
            raise forms.ValidationError('La edad no puede ser negativa')
        
        if edad > 216:  # 18 años
            raise forms.ValidationError('La edad máxima es 216 meses (18 años)')
        
        return edad

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        
        # Si no hay imagen nueva (campo vacío) y estamos editando, mantener la imagen actual
        if not imagen:
            if self.instance and self.instance.pk and self.instance.imagen:
                return self.instance.imagen  # Mantener la imagen existente
            else:
                raise forms.ValidationError("La imagen es obligatoria.")
        
        # Si es una nueva imagen subida (UploadedFile)
        if hasattr(imagen, 'content_type'):
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
            if imagen.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Tipo de archivo no permitido. Solo se permiten imágenes JPG, PNG, WEBP y GIF."
                )
            
            # Validar tamaño del archivo (máximo 5MB)
            max_size = 5 * 1024 * 1024  # 5MB en bytes
            if imagen.size > max_size:
                raise forms.ValidationError(
                    "El archivo es demasiado grande. El tamaño máximo permitido es 5MB."
                )
            
            # Validar dimensiones de la imagen
            try:
                from PIL import Image
                img = Image.open(imagen)
                
                # Verificar que es una imagen válida
                img.verify()
                
                # Reabrir la imagen para obtener dimensiones (verify() cierra el archivo)
                imagen.seek(0)
                img = Image.open(imagen)
                width, height = img.size
                
                # Validar dimensiones mínimas
                min_width, min_height = 100, 100
                if width < min_width or height < min_height:
                    raise forms.ValidationError(
                        f"La imagen debe tener al menos {min_width}x{min_height} píxeles. "
                        f"Dimensiones actuales: {width}x{height}."
                    )
                
                # Validar dimensiones máximas
                max_width, max_height = 4000, 4000
                if width > max_width or height > max_height:
                    raise forms.ValidationError(
                        f"La imagen es demasiado grande. Las dimensiones máximas son {max_width}x{max_height} píxeles. "
                        f"Dimensiones actuales: {width}x{height}."
                    )
                    
            except Exception as e:
                raise forms.ValidationError(
                    "No se pudo procesar la imagen. Asegúrate de que sea un archivo de imagen válido."
                )
            
            # Resetear la posición del archivo después de las validaciones
            imagen.seek(0)
        
        # Si llegamos aquí, la imagen es válida (nueva o existente)
        return imagen

    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        
        # Validaciones cruzadas si es necesario
        edad_meses = cleaned_data.get('edad_meses')
        genero = cleaned_data.get('genero')
        
        # Ejemplo: validaciones específicas según edad y género
        if edad_meses is not None and edad_meses < 6:
            # Para bebés menores de 6 meses, podríamos necesitar validaciones especiales
            if not cleaned_data.get('observaciones_adicionales'):
                self.add_error(
                    'observaciones_adicionales', 
                    'Para bebés menores de 6 meses, se requiere información adicional'
                )
        
        return cleaned_data

    def save(self, commit=True):
        """Guardar el análisis con datos adicionales"""
        analisis = super().save(commit=False)
        
        # Si es un nuevo análisis, inicializar campos por defecto
        if not analisis.pk:
            # Los resultados de IA se llenarán después del procesamiento
            analisis.estado_nutricional = 2  # Normal por defecto
            analisis.confianza = 0.0
        
        if commit:
            analisis.save()
            
        return analisis


class AnalisisEditarForm(AnalisisNutricionalForm):
    """Formulario especializado para editar análisis existentes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Para edición, la imagen no es requerida si ya existe
        self.fields['imagen'].required = False
        
        # Agregar campos adicionales que solo aparecen en edición
        self.fields['estado_nutricional'] = forms.ChoiceField(
            choices=AnalisisNutricional.ESTADO_CHOICES,
            widget=forms.Select(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20'
            }),
            required=False,
            label='Estado Nutricional'
        )
        
        self.fields['confianza'] = forms.FloatField(
            widget=forms.NumberInput(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20',
                'step': '0.01',
                'min': '0',
                'max': '1'
            }),
            required=False,
            label='Confianza (0.0 - 1.0)'
        )
        
        self.fields['severidad'] = forms.ChoiceField(
            choices=[('', 'Sin definir')] + list(AnalisisNutricional.SEVERIDAD_CHOICES),
            widget=forms.Select(attrs={
                'class': 'w-full glass rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20'
            }),
            required=False,
            label='Severidad'
        )

    class Meta(AnalisisNutricionalForm.Meta):
        fields = AnalisisNutricionalForm.Meta.fields + [
            'estado_nutricional', 
            'confianza', 
            'severidad'
        ]


class FiltroAnalisisForm(forms.Form):
    """Formulario para filtrar la lista de análisis"""
    
    buscar = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg px-4 py-2 border border-gray-300 focus:ring-2 focus:ring-primary/50',
            'placeholder': 'Buscar por nombre o observaciones...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + list(AnalisisNutricional.ESTADO_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full rounded-lg px-4 py-2 border border-gray-300 focus:ring-2 focus:ring-primary/50'
        })
    )
    
    severidad = forms.ChoiceField(
        choices=[('', 'Todas las severidades')] + list(AnalisisNutricional.SEVERIDAD_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full rounded-lg px-4 py-2 border border-gray-300 focus:ring-2 focus:ring-primary/50'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full rounded-lg px-4 py-2 border border-gray-300 focus:ring-2 focus:ring-primary/50',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full rounded-lg px-4 py-2 border border-gray-300 focus:ring-2 focus:ring-primary/50',
            'type': 'date'
        })
    )