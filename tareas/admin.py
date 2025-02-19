from django.contrib import admin
from .models import Activo,Task
from django.utils import timezone
from django.utils.html import format_html
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from import_export.admin import ImportExportModelAdmin

class TaskAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    exclude = ('user',)  # Excluye el campo "usuario" del formulario de administración
    readonly_fields = ('user','created_at','completed_at', 'completed_user',)  # Hace que el campo "usuario" sea de solo lectura

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

    def state_color(self, obj):
        if obj.state == 'PENDIENTE':
            return 'pendiente-rojo'  # Define la clase CSS para el estado 'Pendiente'
        elif obj.state == 'PROCESO':
            return 'proceso-amarillo'  # Define la clase CSS para el estado 'En proceso'
        elif obj.state == 'COMPLETADA':
            return 'completada-verde'  # Define la clase CSS para el estado 'Terminado'
        return ''

    def state_color_css(self, obj):
        return format_html('<span class="{}">{}</span>', self.state_color(obj), obj.get_state_display())

    state_color_css.allow_tags = True
    state_color_css.short_description = 'Estado'

    def custom_created_at(self, obj): # Solo fecha sin hora
        return obj.created_at.date() if obj.created_at else None

    custom_created_at.short_description = 'FECHA PEDIDO'

    def days_since_created(self, obj):
        if obj.created_at:
            today = timezone.now().date()
            delta = today - obj.created_at.date()
            return delta.days
        return None

    days_since_created.short_description = 'DÍAS PENDIENTES'

    search_fields = ['maquina__nombre']
    list_display = ('maquina','description','custom_created_at','days_since_created','tipo','priority_color_css', 'state_color_css', 'user', 'completed_user')
    list_filter = (('state',MultiSelectFieldListFilter), 'tipo','priority',)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.state == 'COMPLETADA':
            return False  # Deniega la eliminación de tareas marcadas como "COMPLETADAS"
        return True

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva tarea
             obj.user = request.user  # Asigna el usuario logueado
             if 'state' in form.changed_data and form.cleaned_data['state'] == 'COMPLETADA':
                 obj.completed_user = request.user
                 obj.completed_at = timezone.now()  # Establece la fecha actual como fecha de finalización
        else:
            if 'state' in form.changed_data and form.cleaned_data['state'] == 'COMPLETADA':
                obj.completed_user = request.user
                obj.completed_at = timezone.now()  # Establece la fecha actual como fecha de finalización
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.state == 'COMPLETADA':
            return self.readonly_fields + ('maquina','tipo','description', 'priority', 'state')
        return self.readonly_fields

admin.site.site_header = 'Sistema de gestión de tareas'
admin.site.index_title = 'Área de características'                 # default:
admin.site.site_title = 'Sistema de gestión' # default: "Django site admin"
admin.site.register(Task,TaskAdmin)
admin.site.register(Activo)