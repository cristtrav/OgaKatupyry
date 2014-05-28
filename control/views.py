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
    #Se comprueba que el POST tenga los dos parametros necesarios
    if request.POST.has_key('numeroPuerto') and request.POST.has_key('idregistro'):
        nrp = int(request.POST.get('numeroPuerto'))#Se guarda el puerto actual a operar
        idreg = int(request.POST.get('idregistro'))#Se guarda el id del registro de trabajo
        
        print ("Numero puerto recibido: "+str(nrp))#Se imprime el numero de puerto recibido
        print ("id recibido: "+str(idreg))#Se imprime el numero de puerto recibido
        
        #Se carga el registro de la base de datos segun el codigo enviado
        regActual = configPuerto.objects.filter(id = idreg).first()
        
        print ("Id obtenido de la bd: "+str(regActual.id))#Se imprime el ID recibido
        
        if(nrp==regActual.puertoon):#Se comprueba si la accion es ON
            regActual.ultestado = True #Se actualiza el dato
            regActual.save() #Se guarda en la base de datos
        elif(nrp == regActual.puertooff):# Se comprueba si la accion es OFF
            regActual.ultestado = False #se actualiza el dato
            regActual.save()#Se guarda en la base de datos
        
        if(gpio_disponible):#Se comprueba si la libreria RPi.GPIO esta instalada
            GPIO.output(nrp, GPIO.LOW)#Se activa la salida correspondiente
            time.sleep(2)#Se pausa el programa 2 segundos
            GPIO.output(nrp, GPIO.HIGH)#Se desactiva la salida correspondiente
        else:#En caso de no estar instalada la libreria RPi.GPIO
            print("No se puede activar el puerto: RPi.GPIO no instalado")
        infoPuerto = {#Se crea el objeto JSON para enviar a la pagina
            "puertoActual": nrp,
        }
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")#Se envia el objeto JSON
    else:#Ocurre si no se eviaron datos para un puerto
        print("No se encontraron todas las claves en el post")
        return HttpResponseRedirect("/control/")

def acerca(request):
    return render(request, 'acerca.html')
    