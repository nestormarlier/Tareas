from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

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
        maquina = models.ForeignKey(Activo,on_delete=models.CASCADE, null=True, blank=True, verbose_name='Activo')
        tipo = models.CharField(max_length=10, choices=TIPO_TAREA)
        description = models.TextField(verbose_name='Descripción')
        priority = models.CharField(max_length=10,default='ALTA',choices=ORDEN_PRIORIDAD,verbose_name='Prioridad')
        state = models.CharField(max_length=50, default='PENDIENTE',null=True, blank=True, choices=ESTADO_TAREA, verbose_name='Estado')
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
        completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Completada')
        completed_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='tasks_completed',verbose_name='Usuario Realizo')
        dias_transcurridos = models.IntegerField(default=0)
        latitude = models.FloatField(null=True, blank=True)
        longitude = models.FloatField(null=True, blank=True)

        def __str__(self):
            return str(self.id) + '-' + self.description
        
        class Meta:
            verbose_name_plural = 'Tareas'

class TaskFile(models.Model):
            task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='archivos')
            archivo = models.FileField(upload_to='tareas_adjuntos/', verbose_name='Archivo Adjunto')

            def es_imagen(self):
                return self.archivo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

            def __str__(self):
                return self.archivo.name if self.archivo else "Sin archivo"
            
            class Meta:
                verbose_name_plural = 'Archivos Adjuntos'

@receiver(post_delete, sender=TaskFile)
def eliminar_archivo(sender, instance, **kwargs):
    if instance.archivo:
        instance.archivo.delete(False)