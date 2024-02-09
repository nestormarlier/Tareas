from django.shortcuts import render

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Task
from django.db import models

def tarea_x_estado(request):
    
    tareas = Task.objects.all()

    tareas_completadas = tareas.filter(state = "COMPLETADA")
    tareas_pendientes = tareas.filter(state = "PENDIENTE")
    tareas_proceso = tareas.filter(state = "PROCESO")

    total_completadas = tareas_completadas.count()
    total_pendientes = tareas_pendientes.count()
    total_proceso = tareas_proceso.count()

    total_por_estado =[total_completadas,total_pendientes,total_proceso]

    return render(request, 'tareas/graficos.html', {'totales_por_estado': total_por_estado})