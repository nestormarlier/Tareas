from django.urls import path
from .views import tarea_x_estado

urlpatterns = [
    path('', tarea_x_estado, name="tareas")
]