from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from models import configPuerto
import time

#Se comprueba si esta instalada la libreria RPi.GPIO
try:
    import RPi.GPIO as GPIO
    gpio_disponible = True
except ImportError:
    gpio_disponible = False

# Create your views here.
def control(request):    
    cfgpuertosbd = configPuerto.objects.all()#Se obtienen todos los puertos de la base de datos
    #Se envian como parametros a la plantilla el estado actual de los puertos y los puertos configurados para construir la pagina
    return render(request, "control.html", {"puertos" : cfgpuertosbd,})

def accionarControl(request):
    print("accionarControl llamado")    
    if request.POST.has_key('numeroPuerto'):
        nrp = int(request.POST.get('numeroPuerto'))#Se guarda el puerto actual a operar
        print ("Numero puerto recibido: "+str(nrp))#Se imprime el numero de puerto recibido
        
        if(gpio_disponible):
            GPIO.output(nrp, GPIO.LOW)
            time.sleep(10)
            GPIO.output(nrp, GPIO.HIGH)
        else:
            print("No se puede activar el puerto: RPi.GPIO no instalado")
        infoPuerto = {#Se crea el objeto JSON para enviar a la pagina
            "puertoActual": nrp,
        }
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")#Se envia el objeto JSON
    else:#Ocurre si no se eviaron datos para un puerto
        return HttpResponseRedirect("/control/")

def acerca(request):
    return render(request, 'acerca.html')
    