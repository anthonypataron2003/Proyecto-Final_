from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import os
from apps.recursos.models import RecursoEducativo
from apps.recursos.forms.RecursosForm import RecursoEducativoForm

def recursos_educativos(request):
    """Vista principal para mostrar todos los recursos educativos"""
    recursos = RecursoEducativo.objects.filter(activo=True)
    
    
    categoria = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    orden = request.GET.get('orden', 'newest')
    
    if categoria:
        recursos = recursos.filter(categoria=categoria)
    
    if busqueda:
        recursos = recursos.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    if orden == 'newest':
        recursos = recursos.order_by('-fecha_creacion')
    elif orden == 'oldest':
        recursos = recursos.order_by('fecha_creacion')
    elif orden == 'title':
        recursos = recursos.order_by('titulo')
    elif orden == 'popular':
        recursos = recursos.order_by('-visualizaciones', '-descargas')
    
    paginator = Paginator(recursos, 12)  
    page_number = request.GET.get('page')
    recursos_paginados = paginator.get_page(page_number)
    
    total_recursos = RecursoEducativo.objects.filter(activo=True).count()
    categorias_count = RecursoEducativo.objects.filter(activo=True).values('categoria').distinct().count()
    
    context = {
        'recursos': recursos_paginados,
        'total_recursos': total_recursos,
        'categorias_count': categorias_count,
        'categoria_actual': categoria,
        'busqueda_actual': busqueda,
        'orden_actual': orden,
        'categorias': RecursoEducativo.CATEGORIA_CHOICES,
    }
    
    return render(request, 'recursos/recursos_educativos.html', context)

def detalle_recurso(request, pk):
    """Vista para mostrar el detalle de un recurso específico"""
    recurso = get_object_or_404(RecursoEducativo, pk=pk, activo=True)
    
    recurso.visualizaciones = F('visualizaciones') + 1
    recurso.save(update_fields=['visualizaciones'])
    
    recursos_relacionados = RecursoEducativo.objects.filter(
        categoria=recurso.categoria,
        activo=True
    ).exclude(pk=recurso.pk)[:4]
    
    context = {
        'recurso': recurso,
        'recursos_relacionados': recursos_relacionados,
    }
    
    return render(request, 'recursos/detalle_recurso.html', context)

@login_required
def crear_recurso(request):
    """Vista para crear un nuevo recurso educativo (solo staff)"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para crear recursos.')
        return redirect('recursos_educativos')
    
    if request.method == 'POST':
        form = RecursoEducativoForm(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.creado_por = request.user
            recurso.save()
            messages.success(request, f'Recurso "{recurso.titulo}" creado exitosamente.')
            return redirect('recursos:recursos_educativos')
    else:
        form = RecursoEducativoForm()
    
    return render(request, 'recursos/crear_recursos.html', {'form': form})

@login_required
def editar_recurso(request, pk):
    """Vista para editar un recurso existente (solo staff)"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para editar recursos.')
        return redirect('recursos:recursos_educativos')
    
    recurso = get_object_or_404(RecursoEducativo, pk=pk)
    
    if request.method == 'POST':
        form = RecursoEducativoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Recurso "{recurso.titulo}" actualizado exitosamente.')
            return redirect('recursos:detalle_recurso', pk=recurso.pk)
    else:
        form = RecursoEducativoForm(instance=recurso)
    
    return render(request, 'recursos/editar_recurso.html', {
        'form': form,
        'recurso': recurso
    })

@login_required
def eliminar_recurso(request, pk):
    """Vista para eliminar un recurso (solo staff)"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar recursos.')
        return redirect('recursos_educativos')
    
    recurso = get_object_or_404(RecursoEducativo, pk=pk)
    
    if request.method == 'POST':
        titulo = recurso.titulo
        recurso.activo = False  
        recurso.save()
        messages.success(request, f'Recurso "{titulo}" eliminado exitosamente.')
        return redirect('recursos:recursos_educativos')
    
    return render(request, 'recursos/confirmar_eliminacion.html', {'recurso': recurso})

def descargar_recurso(request, pk):
    """Vista para descargar un recurso desde S3"""
    recurso = get_object_or_404(RecursoEducativo, pk=pk, activo=True)
    
    recurso.descargas = F('descargas') + 1
    recurso.save(update_fields=['descargas'])
    
    if not recurso.archivo:
        raise Http404("El archivo no existe")
    
    try:
       
        
        return redirect(recurso.archivo.url)

    except Exception as e:
        print(f"Error al descargar recurso {pk}: {str(e)}")
        raise Http404("Error al acceder al archivo")


def descargar_recurso_privado(request, pk):
    """Vista para descargar un recurso privado usando URL pre-firmada"""
    from django.conf import settings
    import boto3
    from botocore.exceptions import ClientError
    
    recurso = get_object_or_404(RecursoEducativo, pk=pk, activo=True)
    
    recurso.descargas = F('descargas') + 1
    recurso.save(update_fields=['descargas'])
    
    if not recurso.archivo:
        raise Http404("El archivo no existe")
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': recurso.archivo.name
            },
            ExpiresIn=3600  
        )
        
        return redirect(presigned_url)
        
    except ClientError as e:
        print(f"Error al generar URL pre-firmada: {str(e)}")
        raise Http404("Error al acceder al archivo")


def descargar_recurso_directo(request, pk):
    """Vista para servir el archivo directamente desde Django"""
    from django.core.files.storage import default_storage
    
    recurso = get_object_or_404(RecursoEducativo, pk=pk, activo=True)
    
    recurso.descargas = F('descargas') + 1
    recurso.save(update_fields=['descargas'])
    
    if not recurso.archivo:
        raise Http404("El archivo no existe")
    
    try:
        if not default_storage.exists(recurso.archivo.name):
            raise Http404("El archivo no existe en el almacenamiento")
        
        with default_storage.open(recurso.archivo.name, 'rb') as file:
            file_content = file.read()
        
        import mimetypes
        content_type, _ = mimetypes.guess_type(recurso.archivo.name)
        if not content_type:
            content_type = 'application/octet-stream'
        
        response = HttpResponse(file_content, content_type=content_type)
        
        filename = f"{recurso.titulo}.{recurso.extension_archivo.lower()}"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(file_content)
        
        return response
        
    except Exception as e:
        print(f"Error al descargar recurso {pk}: {str(e)}")
        raise Http404("Error al acceder al archivo")

@csrf_exempt
def track_recurso_view(request):
    """API endpoint para rastrear visualizaciones de recursos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recurso_id = data.get('recurso_id')
            
            if recurso_id:
                recurso = RecursoEducativo.objects.get(pk=recurso_id, activo=True)
                recurso.visualizaciones = F('visualizaciones') + 1
                recurso.save(update_fields=['visualizaciones'])
                
                return JsonResponse({'status': 'success'})
        except (RecursoEducativo.DoesNotExist, json.JSONDecodeError):
            pass
    
    return JsonResponse({'status': 'error'}, status=400)

def recursos_por_categoria_api(request):
    """API para obtener recursos filtrados por categoría"""
    categoria = request.GET.get('categoria')
    limit = int(request.GET.get('limit', 10))
    
    recursos = RecursoEducativo.objects.filter(activo=True)
    
    if categoria:
        recursos = recursos.filter(categoria=categoria)
    
    recursos = recursos.order_by('-fecha_creacion')[:limit]
    
    recursos_data = []
    for recurso in recursos:
        recursos_data.append({
            'id': recurso.id,
            'titulo': recurso.titulo,
            'categoria': recurso.categoria,
            'descripcion': recurso.descripcion[:100] + '...' if len(recurso.descripcion) > 100 else recurso.descripcion,
            'fecha_creacion': recurso.fecha_creacion.strftime('%d/%m/%Y'),
            'visualizaciones': recurso.visualizaciones,
            'descargas': recurso.descargas,
            'url_descarga': f'/recursos/descargar/{recurso.id}/',
            'url_detalle': f'/recursos/{recurso.id}/',
        })
    
    return JsonResponse({
        'recursos': recursos_data,
        'total': recursos.count()
    })

def estadisticas_recursos(request):
    """Vista para mostrar estadísticas de recursos (solo staff)"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para ver estadísticas.')
        return redirect('recursos:recursos_educativos')
    
    total_recursos = RecursoEducativo.objects.filter(activo=True).count()
    total_descargas = RecursoEducativo.objects.filter(activo=True).aggregate(
        total=models.Sum('descargas')
    )['total'] or 0
    total_visualizaciones = RecursoEducativo.objects.filter(activo=True).aggregate(
        total=models.Sum('visualizaciones')
    )['total'] or 0
    
    recursos_populares = RecursoEducativo.objects.filter(activo=True).order_by(
        '-descargas', '-visualizaciones'
    )[:10]
    
    from django.db.models import Count, Sum
    stats_por_categoria = RecursoEducativo.objects.filter(activo=True).values(
        'categoria'
    ).annotate(
        count=Count('id'),
        total_descargas=Sum('descargas'),
        total_visualizaciones=Sum('visualizaciones')
    ).order_by('-count')
    
    context = {
        'total_recursos': total_recursos,
        'total_descargas': total_descargas,
        'total_visualizaciones': total_visualizaciones,
        'recursos_populares': recursos_populares,
        'stats_por_categoria': stats_por_categoria,
    }
    
    return render(request, 'recursos/estadisticas.html', context)