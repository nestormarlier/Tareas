from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return render(request, 'dashboard.html')

def saludo(self):
    return HttpResponse('<h3>Hola Mundo !!!</h3>')
