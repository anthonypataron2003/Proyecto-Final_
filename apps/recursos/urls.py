from django.urls import path
from apps.recursos.views.CrudRecursos import recursos_educativos, detalle_recurso, crear_recurso, editar_recurso, eliminar_recurso, descargar_recurso, track_recurso_view,recursos_por_categoria_api,estadisticas_recursos

app_name = 'recursos'

urlpatterns = [
    # Vistas principales
    path('', recursos_educativos, name='recursos_educativos'),
    path('<int:pk>/', detalle_recurso, name='detalle_recurso'),
    path('crear/', crear_recurso, name='crear_recurso'),
    path('<int:pk>/editar/', editar_recurso, name='editar_recurso'),
    path('<int:pk>/eliminar/', eliminar_recurso, name='eliminar_recurso'),
    path('descargar/<int:pk>/', descargar_recurso, name='descargar_recurso'),
    
    # API endpoints
    path('api/track-view/', track_recurso_view, name='track_recurso_view'),
    path('api/por-categoria/', recursos_por_categoria_api, name='recursos_por_categoria_api'),
    
    # Estadísticas (solo staff)
    path('estadisticas/', estadisticas_recursos, name='estadisticas_recursos'),
]