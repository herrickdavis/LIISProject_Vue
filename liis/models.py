"""LIIS Models."""
from django.db import models

class Equipo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    codigo_interno = models.CharField(max_length=50, null=True, blank=True)
    equipo = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    unidad = models.CharField(max_length=10)
    extraccion = models.BooleanField(default=True)
    host = models.CharField(max_length=255, null=True, blank=True)
    puerto = models.CharField(max_length=255, null=True, blank=True)
    baudios = models.IntegerField(default=9600)
    pais = models.CharField(max_length=255)
    sede = models.CharField(max_length=255, null=True, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    formato = models.CharField(max_length=100, null=True, blank=True)
    creador = models.CharField(max_length=255)
    update = models.DateTimeField(null=True, blank=True)
    update_user = models.CharField(max_length=255, null=True, blank=True)
    bytesize = models.IntegerField(null=True, blank=True)
    parity = models.CharField(max_length=5, null=True, blank=True)
    stopbits = models.CharField(max_length=3, null=True, blank=True)
    max_value = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = True  # Esto le dice a Django que no gestione las migraciones de este modelo.
        db_table = 'liis_equipo' # Asigna un nombre de tabla explícito si la tabla ya existe en tu DB.

    
    def __str__(self):
        return self.codigo

class Medicion(models.Model):
    
    muestra = models.CharField(max_length=255)
    idve = models.CharField(max_length=255)
    medida =  models.CharField(max_length=10)
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, null=True)
    host = models.CharField(max_length=255, null=True)
    ip_host = models.CharField(max_length=255, null=True)
    creacion = models.DateTimeField(auto_now_add=True)
    creador = models.CharField(max_length=255)
    enviado = models.BooleanField(default=False, null=True)
    
    class Meta:
        managed = True # Esto le dice a Django que no gestione las migraciones de este modelo.
        db_table = 'liis_medicion' 
