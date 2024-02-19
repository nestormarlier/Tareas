from django.urls import path
from .views import tarea_x_estado, home

urlpatterns = [
    path('', tarea_x_estado, name="tareas"),
    path('home/', home, name="home")
]