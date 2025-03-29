from django.urls import path
from .views import tarea_x_estado, eliminar_archivo

urlpatterns = [
    path('', tarea_x_estado, name="tareas"),
    path('eliminar-archivo/<int:archivo_id>/', eliminar_archivo, name='eliminar_archivo')
]