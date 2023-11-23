from django.urls import path
from .views import saludo

urlpatterns = [
    path('main/', saludo)
]