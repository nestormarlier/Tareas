from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render
from .models import Task,TaskFile

def tarea_x_estado(request):
    
    tareas = Task.objects.all()
    total_tareas = tareas.count()

    tareas_completadas = tareas.filter(state = "COMPLETADA")
    tareas_pendientes = tareas.filter(state = "PENDIENTE")
    tareas_proceso = tareas.filter(state = "PROCESO")

    total_completadas = tareas_completadas.count()
    total_pendientes = tareas_pendientes.count()
    total_proceso = tareas_proceso.count()

    total_por_estado =[total_completadas,total_pendientes,total_proceso]

    tareas_correctivas = tareas.filter(tipo='CORRECTIVA')
    tareas_preventivas = tareas.filter(tipo='PREVENTIVA')
    tareas_predictiva = tareas.filter(tipo='PREDICTIVA')
    tareas_otro = tareas.filter(tipo='OTRO')

    total_correctiva= tareas_correctivas.count()
    total_preventivas=tareas_preventivas.count()
    total_predictivas=tareas_predictiva.count()
    total_otro=tareas_otro.count()

    total_por_tipo = [total_correctiva,total_preventivas,total_predictivas,total_otro]

    tareas_alta = tareas.filter(priority='ALTA')
    tareas_media = tareas.filter(priority='MEDIA')
    tareas_baja = tareas.filter(priority='BAJA')

    total_alta=tareas_alta.count()
    total_media=tareas_media.count()
    total_baja=tareas_baja.count()

    total_por_prioridad = [total_alta,total_media,total_baja]
    
    return render(request, 'tareas/graficos.html', {
        'total_completadas' : total_completadas,
        'total_pendientes': total_pendientes,
        'total_proceso':total_proceso,
        'total_tareas': total_tareas,
        'totales_por_estado': total_por_estado,
        'totales_por_tipo': total_por_tipo,
        'totales_por_prioridad': total_por_prioridad
        })

def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(TaskFile, id=archivo_id)
    if request.method == 'POST':
        archivo.archivo.delete()  # Eliminar archivo del servidor
        archivo.delete()  # Eliminar registro de la base de datos
        messages.success(request, "Archivo eliminado correctamente.")
    return redirect(request.META.get('HTTP_REFERER', '/'))