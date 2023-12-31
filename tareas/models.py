from django.db import models
from django.contrib.auth.models import User

class Activo(models.Model):
     nombre=models.CharField(max_length=100, blank=False)

     def __str__(self):
          return self.nombre

class Task(models.Model):
        ORDEN_PRIORIDAD = (
        ('ALTA','ALTA'),
        ('MEDIA','MEDIA'),
        ('BAJA','BAJA')
    )
        ESTADO_TAREA = (
            ('PENDIENTE', 'Pendiente'),
            ('PROCESO', 'En proceso'),
            ('COMPLETADA', 'Completada')
    )
        TIPO_TAREA = (
        ('OTRO', 'Otro'),
        ('CORRECTIVA', 'Correctiva'),
        ('PREVENTIVA', 'Preventiva'),
        ('PREDICTIVA', 'Predictiva')
    )

        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created', verbose_name='Usuario Crea')
        maquina = models.ForeignKey(Activo,on_delete=models.CASCADE, null=True, blank=True)
        tipo = models.CharField(max_length=10, choices=TIPO_TAREA)
        description = models.TextField(verbose_name='Descripción')
        priority = models.CharField(max_length=10,default='ALTA',choices=ORDEN_PRIORIDAD,verbose_name='Prioridad')
        state = models.CharField(max_length=50, default='PENDIENTE',null=True, blank=True, choices=ESTADO_TAREA, verbose_name='Estado')
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
        completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Completada')
        completed_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='tasks_completed',verbose_name='Usuario Realizo')
        dias_transcurridos = models.IntegerField(default=0)

        def __str__(self):
            return str(self.id) + '-' + self.description
        
        class Meta:
            verbose_name_plural = 'Tareas'