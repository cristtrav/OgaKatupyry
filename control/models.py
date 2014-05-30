from django.db import models

# Create your models here.
#Modelo que representa los datos de los puertos habilitados guardados en la base de datos
class configPuerto(models.Model): 
    nropuerto = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    
class usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    nivel = models.IntegerField()
    #def _unicode_(self):
     #   return self.usuario
    