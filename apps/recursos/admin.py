from django.contrib import admin
from apps.recursos.models import RecursoEducativo

@admin.register(RecursoEducativo)
class RecursoEducativoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'categoria', 'creado_por', 'fecha_creacion', 
        'visualizaciones', 'descargas', 'activo'
    ]
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['activo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'visualizaciones', 'descargas']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'categoria', 'descripcion')
        }),
        ('Archivo', {
            'fields': ('archivo',)
        }),
        ('Metadatos', {
            'fields': ('creado_por', 'activo'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('visualizaciones', 'descargas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)