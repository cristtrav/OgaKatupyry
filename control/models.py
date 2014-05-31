from django.db import models

# Create your models here.
#Modelo que representa los datos de los puertos habilitados guardados en la base de datos
class configPuerto(models.Model): 
    puertoon = models.IntegerField()
    puertooff = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    ultestado = models.BooleanField(default=False)
    
class usuario(models.Model):
    usuario = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=30)
    nivel = models.IntegerField()