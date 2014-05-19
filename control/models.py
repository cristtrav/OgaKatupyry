from django.db import models

# Create your models here.
#Modelo que representa los datos de los puertos habilitados guardados en la base de datos
class configPuerto(models.Model): 
    nropuerto = models.IntegerField()
    descripcion = models.CharField(max_length=50)