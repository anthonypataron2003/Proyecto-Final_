from django import forms
from django.core.validators import validate_email

class EnviarAnalisisEmailForm(forms.Form):
    """Formulario para enviar análisis por email"""
    
    destinatario = forms.EmailField(
        label='Email del destinatario',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'required': True
        }),
        help_text='Ingresa el email donde se enviará el análisis'
    )
    
    asunto = forms.CharField(
        label='Asunto',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Resultado de Análisis Nutricional'
        }),
        required=False,
        help_text='Si no especificas, se usará un asunto por defecto'
    )
    
    mensaje_personalizado = forms.CharField(
        label='Mensaje adicional (opcional)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Mensaje adicional que deseas incluir...'
        }),
        required=False,
        help_text='Mensaje personalizado para acompañar el análisis'
    )
    
    incluir_imagen = forms.BooleanField(
        label='Incluir imagen analizada',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Adjuntar la imagen que fue analizada'
    )
    
    incluir_recomendaciones = forms.BooleanField(
        label='Incluir recomendaciones nutricionales',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Incluir las recomendaciones nutricionales en el email'
    )

    def clean_destinatario(self):
        """Validación adicional para el email"""
        email = self.cleaned_data.get('destinatario')
        if email:
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError('Por favor ingresa un email válido.')
        return email