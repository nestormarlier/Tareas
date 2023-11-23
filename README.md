# Tareas
Sistema de seguimientos de tareas con estados, tipos, prioridad por máquina y/o activo 
Usar Django Django==4.0.6 --> ya que el deploy esta en pythonanywhere que es el que soporta
la carpeta templates debe ir en settings.py la direccion exacta para que funcione
pip install django_admin_multi_select_filter --> para que funcione el multipleselect
pip install pip install django-import_export
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/envaplastsrl/Tareas/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
-
