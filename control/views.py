from django.shortcuts import render
from django.http import HttpResponse
import json
from models import configPuerto, usuario
#DESCOMENTAR LA SIGUEIENTE LINEA CUANDO SE DESPLIEGA EN EL RASPBERRY CONTANDO CON LA LIBRERIA RPi.GPIO
#import RPi.GPIO as GPIO

# Create your views here.
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
        cfgpuertos = configPuerto.objects.all()
        return render(request, "control.html", {"puertos" : cfgpuertos})

def acerca(request):
    return render(request, 'acerca.html')
        
    
def loginget(request):   
    if request.method == "POST":
        
        if request.POST.has_key('usuariof') and request.POST.has_key('passwordf'):
             x=request.POST.get('usuariof')
             y=request.POST.get('passwordf')
             print("usuariof"+x)
             print("passwordf"+y)
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
        print("es el get")
     
    #usr = usuario.objects.all()
    #return render(request, 'login.html', {"users": usr})    

def log(request):
    return render(request, 'login.html')