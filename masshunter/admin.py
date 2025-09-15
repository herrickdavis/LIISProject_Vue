# masshunter/admin.py
from django.contrib import admin
from .models import Pais, Instrumento, Metodo, Configuracion

admin.site.register(Pais)
admin.site.register(Instrumento)
admin.site.register(Metodo)
admin.site.register(Configuracion)