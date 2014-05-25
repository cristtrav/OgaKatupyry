from django.shortcuts import render
from django.http import HttpResponse
import json
from models import configPuerto

#Se comprueba si está instalada la libreria RPi.GPIO
try:
    import RPi.GPIO as GPIO
    gpio_disponible = True
except ImportError:
    gpio_disponible = False

# Create your views here.
def control(request):    
    cfgpuertos = configPuerto.objects.all()
    return render(request, "control.html", {"puertos" : cfgpuertos})
    
def accionarControl(request):
    print("accionarControl llamado")    
    if request.POST.has_key('opcionPuerto') and request.POST.has_key('numeroPuerto'):
        opp = request.POST.get('opcionPuerto', 'nada')#Se guarda la accion a realizar con el puerto
        nrp = request.POST.get('numeroPuerto')#Se guarda el puerto actual a operar
        
        print ("Dato recibido: "+opp)#Se imprime la accion a realizar
        print ("Numero puerto recibido: "+nrp)#Se imprime el numero de puerto recibido
        
        estadoPuerto = '0';#Se creea la variable para guardar el estado del puerto a enviar
        if(opp == 'true'):#Se comprueba la opcion enviada por la página
            estadoPuerto = '1'
            if gpio_disponible: #Si está instalada la libreria RPi.GPIO se cambia el estado del puerto
                GPIO.output(nrp, GPIO.HIGH)
            else:#Si no está instalada la libreria RPi.GPIO se muestra un mensaje
                print("No se puede activar el puerto: RPi.GPIO no instalado")
            
        else:
            estadoPuerto = '0'
            
            if gpio_disponible:#Si está instalada la libreria RPi.GPIO se cambia el estado del puerto
                GPIO.output(nrp, GPIO.LOW)
            else:#Si no está instalada la libreria RPi.GPIO se muestra un mensaje
                print("No se puede desactivar el puerto: RPi.GPIO no instalado")
            
            #DESCOMENTAR LA SIGUEIENTE LINEA CUANDO SE DESPLIEGA EN EL RASPBERRY CONTANDO CON LA LIBRERIA RPi.GPIO
            
        if(gpio_disponible):#Si está instalada la libreria RPi.GPIO se cambia el estado del puerto
            estadoPuerto = str(GPIO.input(nrp))#Se lee el estado actual del puerto actual
        else:#Si no está instalada la libreria RPi.GPIO se muestra un mensaje
            print("No se puede leer estado del puerto: RPi.GPIO no instalado")
        
        infoPuerto = {#Se crea el objeto JSON para enviar a la página
            "estadoActual": estadoPuerto,
            "puertoActual": nrp,
        }
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")#Se envia el objeto JSON
    else:#Ocurre si no se eviaron datos para un puerto
        print("No existe clave 'opcionPuerto'")
        cfgpuertos = configPuerto.objects.all()
        return render(request, "control.html", {"puertos" : cfgpuertos})

def acerca(request):
    return render(request, 'acerca.html')
    