from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from models import configPuerto
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def update(request):
        query = configPuerto.objects.all()
        return render(request, 'update.html', {"puertos" : query } )

def deleteall(request):
    del_puertos = configPuerto.object.all().delete()
    return render (request, "Configuracion.html")

def savePuertos(request):
    bart = configPuerto.objects.all()
    return render(request, "savePuertos.html", {"opciones" : bart})
 
def configuracion(request):
    consulta = configPuerto.objects.all()
    return render(request, "Configuracion.html", {"puertos" : consulta})
    

def control(request):    
    cfgpuertos = configPuerto.objects.all()
    return render(request, "control.html", {"puertos" : cfgpuertos})
    
def accionarControl(request):
    print("accionarControl llamado")    
    if request.POST.has_key('opcionPuerto') and request.POST.has_key('numeroPuerto'):
        opp = request.POST.get('opcionPuerto', 'nada')
        nrp = request.POST.get('numeroPuerto')
        
        print ("Dato recibido: "+opp)
        print ("Numero puerto recibido: "+nrp)
        
        estadoPuerto = '0';
        if(opp == 'true'):
            estadoPuerto = '1'
            #DESCOMENTAR LA SIGUEIENTE LINEA CUANDO SE DESPLIEGA EN EL RASPBERRY CONTANDO CON LA LIBRERIA RPi.GPIO
            #GPIO.output(nrp, GPIO.HIGH)
        else:
            estadoPuerto = '0'
            #GPIO.output(nrp, GPIO.LOW)
        #DESCOMENTAR LA SIGUEIENTE LINEA CUANDO SE DESPLIEGA EN EL RASPBERRY CONTANDO CON LA LIBRERIA RPi.GPIO
        #estadoPuerto = str(GPIO.input(nrp))
        infoPuerto = {
            "estadoActual": estadoPuerto,
            "puertoActual": nrp,
        }
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")
    else:
        print("No existe clave 'opcionPuerto'")
        return render(request, "control.html")
    

    