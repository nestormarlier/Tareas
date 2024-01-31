from django.shortcuts import render

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Task
from django.db import models

def generar_grafico(request):
    # Datos de ejemplo (puedes reemplazarlos con tus datos reales de la base de datos)
    estados = ['Completada', 'Pendiente', 'En proceso']
    prioridades = ['Alta', 'Baja', 'Media']
    tipos = ['Otro', 'Correctiva', 'Preventiva', 'Predictiva']

    # Cuenta de tareas por estado
    # tareas_por_estado = [10, 20, 15]
    recuentos_por_estado = Task.objects.values('state').annotate(total_tareas=models.Count('id'))
    tareas_por_estado = [entry['total_tareas'] for entry in recuentos_por_estado]

    # Cuenta de tareas por prioridad
    # tareas_por_prioridad = [5, 10, 30]
    recuentos_por_prioridad = Task.objects.values('priority').annotate(total_tareas=models.Count('id'))
    tareas_por_prioridad = [entry['total_tareas'] for entry in recuentos_por_prioridad]

    # Cuenta de tareas por tipo
    tareas_por_tipo = [8, 15, 12, 25]  # Reemplaza con tus datos reales

    # Generar gráficos
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    axs[0].bar(estados, tareas_por_estado, color='blue')
    axs[0].set_title('Tareas por Estado')

    axs[1].bar(prioridades, tareas_por_prioridad, color='green')
    axs[1].set_title('Tareas por Prioridad')

    axs[2].bar(tipos, tareas_por_tipo, color='orange')
    axs[2].set_title('Tareas por Tipo')

    # Guardar la imagen en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la imagen a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'tareas/graficos.html', {'graphic': graphic})