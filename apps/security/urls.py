from django.urls import path
from apps.security.views import CustomLoginView, CustomRegisterView, custom_logout_view

app_name = 'security'

urlpatterns = [
    # Usando vistas basadas en clases
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', custom_logout_view, name='logout'),
]
