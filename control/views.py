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
    if request.POST.has_key('numeroPuerto') and request.POST.has_key('idregistro'):
        nrp = int(request.POST.get('numeroPuerto'))#Se guarda el puerto actual a operar
        idreg = int(request.POST.get('idregistro'))
        
        print ("Numero puerto recibido: "+str(nrp))#Se imprime el numero de puerto recibido
        print ("id recibido: "+str(idreg))#Se imprime el numero de puerto recibido
        
        regActual = configPuerto.objects.filter(id = idreg).first()
        
        print ("Id obtenido de la bd: "+str(regActual.id))
        
        if(nrp==regActual.puertoon):
            regActual.ultestado = True
            regActual.save()
        elif(nrp == regActual.puertooff):
            regActual.ultestado = False
            regActual.save()
        
        if(gpio_disponible):
            GPIO.output(nrp, GPIO.LOW)
            time.sleep(10)
            GPIO.output(nrp, GPIO.HIGH)
        else:
            print("No se puede activar el puerto: RPi.GPIO no instalado")
        infoPuerto = {#Se crea el objeto JSON para enviar a la pagina
            "puertoActual": nrp,
        }
        time.sleep(2)
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")#Se envia el objeto JSON
    else:#Ocurre si no se eviaron datos para un puerto
        print("No se encontraron todas las claves en el post")
        return HttpResponseRedirect("/control/")

def acerca(request):
    return render(request, 'acerca.html')
    