from django.contrib import admin
from .models import Activo,Task, TaskFile
from django.utils import timezone
from django.utils.html import format_html
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str

class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1  # Permitir agregar múltiples archivos en el formulario de tareas
    can_delete = True  # Habilita la opción de eliminar archivos
    fields = ('archivo', 'mostrar_archivo')  # Quitamos DELETE de los fields
    readonly_fields = ('mostrar_archivo',)  # Mostrar archivo en formato visual

    def mostrar_archivo(self, obj):
        if obj.archivo:
            if obj.es_imagen():
                return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.archivo.url)
            elif obj.archivo.name.lower().endswith('.pdf'):
                return format_html('<iframe src="{}" style="width: 100px; height: 100px; border: none;"></iframe>', obj.archivo.url)
            else:
                return format_html('<a href="{}" target="_blank">Ver archivo</a>', obj.archivo.url)
        return "Sin archivo adjunto"

    mostrar_archivo.short_description = 'Vista previa'

class TaskAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    exclude = ('user',)  # Excluye el campo "usuario" del formulario de administración
    list_display = ('maquina','description','mostrar_ubicacion','custom_created_at','days_since_created','tipo','mostrar_adjuntos','priority_color_css', 'state_color_css', 'user', 'completed_user')
    readonly_fields = ('user','created_at','completed_at','completed_user','dias_transcurridos')  # Hace que el campo "usuario" sea de solo lectura
    inlines = [TaskFileInline] # Archivos adjuntos
    
    class Media:
        js = ('admin/js/geolocation.js',)  # Add custom JavaScript file

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'latitude' in form.base_fields:
            form.base_fields['latitude'].widget.attrs['id'] = 'id_latitude'
        if 'longitude' in form.base_fields:
            form.base_fields['longitude'].widget.attrs['id'] = 'id_longitude'
        return form

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

    def mostrar_ubicacion(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<a href="{}" target="_blank" title="Ver en Google Maps">'
                '<i class="fas fa-map-marker-alt" style="color: red; font-size: 20px;"></i>'
                '</a>',
                url
            )
        return "Sin ubicación"

    mostrar_ubicacion.short_description = 'Ubicación'
    mostrar_ubicacion.allow_tags = True

    def exportar_tareas_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tareas_con_ubicacion.csv"'
        writer = csv.writer(response)
        
        # Escribir encabezados
        writer.writerow([
            smart_str("ID"),
            smart_str("Máquina"),
            smart_str("Descripción"),
            smart_str("Tipo"),
            smart_str("Prioridad"),
            smart_str("Estado"),
            smart_str("Fecha Creación"),
            smart_str("Latitud"),
            smart_str("Longitud"),
            smart_str("Enlace Google Maps")
        ])
        
        # Escribir datos
        for obj in queryset:
            writer.writerow([
                smart_str(obj.id),
                smart_str(obj.maquina),
                smart_str(obj.description),
                smart_str(obj.get_tipo_display()),
                smart_str(obj.get_priority_display()),
                smart_str(obj.get_state_display()),
                smart_str(obj.created_at),
                smart_str(obj.latitude),
                smart_str(obj.longitude),
                smart_str(f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}" if obj.latitude and obj.longitude else "Sin ubicación")
            ])
        
        return response

    exportar_tareas_csv.short_description = "Exportar tareas seleccionadas a CSV"

    actions = [exportar_tareas_csv]

    search_fields = ['maquina__nombre']
    
    list_filter = (('state',MultiSelectFieldListFilter), 'tipo','priority',)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.state == 'COMPLETADA':
            return False  # Deniega la eliminación de tareas marcadas como "COMPLETADAS"
        return True

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva tarea
            obj.user = request.user  # Asigna el usuario logueado
            # Get latitude and longitude from the form data
            obj.latitude = form.cleaned_data.get('latitude')
            obj.longitude = form.cleaned_data.get('longitude')
        if 'state' in form.changed_data and form.cleaned_data['state'] == 'COMPLETADA':
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
            return self.readonly_fields + ('maquina','tipo','description', 'priority', 'state', 'latitude', 'longitude')
        return self.readonly_fields
    
    def mostrar_adjuntos(self, obj):
        archivos = obj.archivos.all()
        if archivos:
            links = []
            for archivo in archivos:
                if archivo.es_imagen():
                    links.append(f'<a href="{archivo.archivo.url}" target="_blank"><img src="{archivo.archivo.url}" style="max-width: 50px; max-height: 50px;" /></a>')
                elif archivo.archivo.name.lower().endswith('.pdf'):
                    links.append(f'<a href="{archivo.archivo.url}" target="_blank"><i class="fas fa-file-pdf" style="color: #ff4444; font-size: 24px;"></i></a>')
                else:
                    links.append(f'<a href="{archivo.archivo.url}" target="_blank">Ver archivo</a>')
            return format_html(' '.join(links))
        return "Sin archivos adjuntos"

    mostrar_adjuntos.short_description = 'Archivos Adjuntos'

admin.site.site_header = 'Sistema de gestión de tareas'
admin.site.index_title = 'Área de características'                 # default:
admin.site.site_title = 'Sistema de gestión' # default: "Django site admin"

# Agregar Font Awesome al panel de administración
admin.site.site_header = format_html(
    '{} <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">',
    admin.site.site_header
)

admin.site.register(Task,TaskAdmin)
# admin.site.register(TaskFile) para eliminar archivos adjuntos por espacio en el servidor
admin.site.register(Activo)