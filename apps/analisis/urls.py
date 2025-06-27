"""
URLs para el módulo de análisis nutricional
"""
from django.urls import path
from apps.analisis.views.analisis import dashboard_estadisticas, descargar_pdf_reporte, enviar_reporte_email, lista_analisis, nuevo_analisis, detalle_analisis, editar_analisis, eliminar_analisis, procesar_imagen_ajax, exportar_reporte

app_name = 'analisis'

urlpatterns = [
    path('', dashboard_estadisticas, name='dashboard'),
    path('estadisticas/', dashboard_estadisticas, name='estadisticas'),
    
    path('lista/', lista_analisis, name='lista'),
    path('nuevo/', nuevo_analisis, name='nuevo'),
    path('<uuid:analisis_id>/', detalle_analisis, name='detalle'),
    path('<uuid:analisis_id>/editar/', editar_analisis, name='editar'),
    path('<uuid:analisis_id>/eliminar/', eliminar_analisis, name='eliminar'),
    
    path('procesar-imagen/', procesar_imagen_ajax, name='procesar_imagen'),
    
    path('exportar/csv/', exportar_reporte, name='exportar_csv'),
    
    path('enviar-email/<uuid:analisis_id>/', enviar_reporte_email, name='enviar_email'),
    
    path('descargar-pdf/<uuid:analisis_id>/', descargar_pdf_reporte, name='descargar_pdf'),
]