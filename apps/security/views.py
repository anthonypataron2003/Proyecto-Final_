from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

from apps.security.forms import CustomAuthenticationForm, CustomUserCreationForm
from apps.security.models import CustomUser

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    """
    Vista personalizada para el login
    """
    form_class = CustomAuthenticationForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('dashboard')  # Cambia por tu URL de dashboard
    
    def dispatch(self, request, *args, **kwargs):
        # Redirigir si ya está autenticado
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Ejecutar cuando el formulario es válido"""
        user = form.get_user()
        login(self.request, user)
        
        messages.success(
            self.request, 
            f'¡Bienvenido de nuevo, {user.first_name}! Has iniciado sesión correctamente.'
        )
        
        logger.info(f'Usuario {user.username} ha iniciado sesión exitosamente')
        
        # Verificar si es una petición AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'¡Bienvenido de nuevo, {user.first_name}!',
                'redirect_url': self.get_success_url()
            })
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ejecutar cuando el formulario es inválido"""
        messages.error(
            self.request, 
            'Error en las credenciales. Por favor, verifica tu usuario y contraseña.'
        )
        
        # Verificar si es una petición AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': 'Error en las credenciales. Por favor, verifica tu usuario y contraseña.'
            })
        
        return super().form_invalid(form)


class CustomRegisterView(CreateView):
    """
    Vista personalizada para el registro
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'account/registro.html'
    success_url = reverse_lazy('security:login')
    
    def dispatch(self, request, *args, **kwargs):
        # Redirigir si ya está autenticado
        if request.user.is_authenticated:
            return redirect('dashboard')  # Cambia por tu URL de dashboard
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Ejecutar cuando el formulario es válido"""
        user = form.save(commit=False)
        user.is_active = True  # El usuario está activo inmediatamente
        user.save()
        
        messages.success(
            self.request, 
            f'¡Cuenta creada exitosamente! Bienvenido a NutriScan Kids, {user.first_name}. Ya puedes iniciar sesión.'
        )
        
        logger.info(f'Nuevo usuario registrado: {user.username} - {user.email}')
        
        # Verificar si es una petición AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'¡Cuenta creada exitosamente! Bienvenido a NutriScan Kids, {user.first_name}.',
                'redirect_url': self.success_url
            })
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ejecutar cuando el formulario es inválido"""
        messages.error(
            self.request, 
            'Error al crear la cuenta. Por favor, revisa los campos marcados en rojo.'
        )
        
        # Verificar si es una petición AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': 'Error al crear la cuenta. Por favor, revisa los campos marcados.'
            })
        
        return super().form_invalid(form)


@login_required
def custom_logout_view(request):
    """
    Vista personalizada para logout
    """
    user_name = request.user.first_name
    logout(request)
    messages.success(request, f'¡Hasta luego, {user_name}! Has cerrado sesión correctamente.')
    return redirect('security:login')