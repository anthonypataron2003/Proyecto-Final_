from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import re

from apps.security.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para registro de usuarios
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Ingrese su nombre completo'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Elija un nombre de usuario único'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    
    # Mantenemos password1 para coincidir con el estándar de Django
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Cree una contraseña segura'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Repita su contraseña'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos.")
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r'\d', password1):
            raise ValidationError("La contraseña debe contener al menos un número.")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        # No necesitamos set_password aquí porque UserCreationForm ya lo maneja
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario personalizado para login
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Ingrese su usuario'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 backdrop-blur-sm',
            'placeholder': 'Ingrese su contraseña'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise ValidationError(
                    "Usuario o contraseña incorrectos. Por favor, verifica tus credenciales.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data