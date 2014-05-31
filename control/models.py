from django.db import models

# Create your models here.
#Modelo que representa los datos de los puertos habilitados guardados en la base de datos
class configPuerto(models.Model): 
    puertoon = models.IntegerField(max_length=10)
    puertoof = models.IntegerField(max_length=10)
    descripcion = models.CharField(max_length=50)