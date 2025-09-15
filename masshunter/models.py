# masshunter/models.py
from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'masshunter_pais'
        verbose_name_plural = "Países"

class Instrumento(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    nombre_equipo = models.CharField(max_length=100)
    nombre_reporte = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_equipo

    class Meta:
        db_table = 'masshunter_instrumento'
        unique_together = ('pais', 'nombre_equipo')

class Metodo(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    metodo_inyeccion = models.CharField(max_length=100)
    metodo_reporte = models.CharField(max_length=100)

    def __str__(self):
        return self.metodo_inyeccion

    class Meta:
        db_table = 'masshunter_metodo'
        unique_together = ('pais', 'metodo_inyeccion')

class Configuracion(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    # En lugar de texto, conectamos con la tabla Instrumento
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE) 
    
    metodo_cuantificacion = models.CharField(max_length=255)
    idve_metodo = models.CharField(max_length=100) # Tu campo "iddmet"
    
    # Tus campos "fini" y "ffin"
    fila_inicio_analitos = models.IntegerField() 
    fila_fin_analitos = models.IntegerField()

    def __str__(self):
        return f"Config para {self.instrumento.nombre_equipo} ({self.pais.codigo})"

    class Meta:
        db_table = 'masshunter_configuracion'
        unique_together = ('instrumento', 'metodo_cuantificacion')