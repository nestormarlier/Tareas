from django.contrib import admin
from .models import Activo,Task
from django.utils import timezone
from django.utils.html import format_html


class TaskAdmin(admin.ModelAdmin):
    exclude = ('user',)  # Excluye el campo "usuario" del formulario de administración
    readonly_fields = ('user','completed_at', 'completed_user',)  # Hace que el campo "usuario" sea de solo lectura
    
    

    def priority_color(self, obj):
        if obj.priority == 'ALTA':
            return 'alta-priority'
        elif obj.priority == 'MEDIA':
            return 'media-priority'
        elif obj.priority == 'BAJA':
            return 'baja-priority'
        return ''

    priority_color.short_description = 'Prioridad'
    
    def priority_color_css(self, obj):
        return format_html('<span class="{}">{}</span>', self.priority_color(obj), obj.get_priority_display())


    priority_color_css.allow_tags = True
    priority_color_css.short_description = 'Prioridad'

    list_display = ('maquina','description','tipo','priority_color_css', 'state', 'user', 'completed_user')
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