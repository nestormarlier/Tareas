from django.urls import path
from .views import generar_grafico

urlpatterns = [
    path('', generar_grafico, name="grafico"),
]