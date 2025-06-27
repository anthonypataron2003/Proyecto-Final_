from django import forms
from apps.recursos.models import RecursoEducativo
import os

class RecursoEducativoForm(forms.ModelForm):
    class Meta:
        model = RecursoEducativo
        fields = ['titulo', 'categoria', 'descripcion', 'archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'glass rounded-xl px-4 py-3 w-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20',
                'placeholder': 'Título del recurso educativo'
            }),
            'categoria': forms.Select(attrs={
                'class': 'glass rounded-xl px-4 py-3 w-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'glass rounded-xl px-4 py-3 w-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20',
                'placeholder': 'Descripción detallada del recurso...',
                'rows': 5
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'glass rounded-xl px-4 py-3 w-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 border border-primary/20',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.jpg,.jpeg,.png'
            })
        }
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño (máximo 10MB)
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 10MB.')
            
            # Validar extensión
            extensiones_permitidas = [
                '.pdf', '.doc', '.docx', '.ppt', '.pptx', 
                '.xls', '.xlsx', '.jpg', '.jpeg', '.png'
            ]
            
            extension = os.path.splitext(archivo.name)[1].lower()
            if extension not in extensiones_permitidas:
                raise forms.ValidationError(
                    f'Formato no permitido. Formatos válidos: {", ".join(extensiones_permitidas)}'
                )
        
        return archivo