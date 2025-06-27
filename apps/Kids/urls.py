from django.urls import path
from apps.Kids import views

urlpatterns = [
    
    # dashboard
    path('', views.dashboard, name='dashboard'),

]