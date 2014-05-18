from django.shortcuts import render
from django.http import HttpResponse
import json
import RPi.GPIO as GPIO

# Create your views here.
def control(request):
    estAct23 = GPIO.input(23)
    valorPuerto23 = 'false'
    if(estAct23 == 0):
        valorPuerto23 = 'false'
    else:
        valorPuerto23 = 'true'
    return render(request, "control.html", {"estadoPuerto23" : valorPuerto23})
    
def accionarControl(request):
    print("accionarControl llamado")    
    if request.POST.has_key('opcionPuerto'):
        opc = request.POST.get('opcionPuerto', 'nada') 
        print ("Dato recibido: "+opc)
        datoEnviar = '0';
        if(opc == 'true'):
            GPIO.output(23, GPIO.HIGH)
        else:
            GPIO.output(23, GPIO.LOW)
        datoEnviar = str(GPIO.input(23))
        return HttpResponse(json.dumps({"estadoActual" : datoEnviar}), content_type="application/json")
    else:
        print("No existe clave 'opcionPuerto'")
        return render(request, "control.html")
    