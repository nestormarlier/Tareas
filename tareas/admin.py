from django.contrib import admin
from .models import Activo,Task
from django.utils import timezone

class TaskAdmin(admin.ModelAdmin):
    exclude = ('user',)  # Excluye el campo "usuario" del formulario de administración
    readonly_fields = ('user','completed_at', 'completed_user',)  # Hace que el campo "usuario" sea de solo lectura
    list_display = ('maquina','description','tipo','priority', 'state', 'user', 'completed_user')
    list_filter = ('state', 'priority','tipo',)  # Agrega el filtro para el campo "tipo"

    def has_delete_permission(self, request, obj=None):
        if obj and obj.state == 'COMPLETADA':
            return False  # Deniega la eliminación de tareas marcadas como "COMPLETADAS"
        return True

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva tarea
            obj.user = request.user  # Asigna el usuario logueado
        else:
            if 'state' in form.changed_data and form.cleaned_data['state'] == 'COMPLETADA':
                obj.completed_user = request.user
                obj.completed_at = timezone.now()  # Establece la fecha actual como fecha de finalización
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.state == 'COMPLETADA':
            return self.readonly_fields + ('description', 'priority', 'state')
        return self.readonly_fields

admin.site.site_header = 'Sistema de gestión de tareas'
admin.site.index_title = 'Área de características'                 # default:
admin.site.site_title = 'Sistema de gestión' # default: "Django site admin"
admin.site.register(Task,TaskAdmin)
admin.site.register(Activo)