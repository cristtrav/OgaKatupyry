# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from models import configPuerto, usuario
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session

#Se comprueba si esta instalada la libreria RPi.GPIO
try:
    import RPi.GPIO as GPIO
    gpio_disponible = True
except ImportError:
    gpio_disponible = False

# Create your views here.
def control(request):
    cfgpuertosbd = configPuerto.objects.all()#Se obtienen todos los puertos de la base de datos
    cfgpuertos = []#Se crea un array para enviar el estado actual de los puertos 
    for p in cfgpuertosbd:#Se recorren todos los puertos obtenidos
        estadoPuerto = 'false'#se carga un valor de estado por default
        if gpio_disponible:#se consulta si esta instalada la libreria RPi.GPIO
            auxEstado = GPIO.input(p.nropuerto)#se lee el estado del puerto actual
            if auxEstado == 1:#Si el estado es activo
                estadoPuerto = 'true'#se carga el valor 'true'
        else:#Si no esta instalada la libreria RPi.GPIO
            print("No se puede leer estado del puerto. RPi.GPIO no instalado")
        auxPuerto = {#se crea un objeto JSON con el numero de puerto y el estado para cambiar los controles de la pagina
                     "puerto": str(p.nropuerto),
                     "estado": estadoPuerto,
        }
        cfgpuertos.append(auxPuerto)#se agrega el objeto al Array
    #Se envian como parametros a la plantilla el estado actual de los puertos y los puertos configurados para construir la pagina
    return render(request, "control.html", {"cfgpuertos" : cfgpuertos,"puertos" : cfgpuertosbd,})
     
def accionarControl(request):
    print("accionarControl llamado")    
    if request.POST.has_key('opcionPuerto') and request.POST.has_key('numeroPuerto'):
        opp = request.POST.get('opcionPuerto', 'nada')#Se guarda la accion a realizar con el puerto
        nrp = int(request.POST.get('numeroPuerto'))#Se guarda el puerto actual a operar
        
        print ("Dato recibido: "+opp)#Se imprime la accion a realizar
        print ("Numero puerto recibido: "+str(nrp))#Se imprime el numero de puerto recibido
        
        estadoPuerto = '0';#Se creea la variable para guardar el estado del puerto a enviar
        if(opp == 'true'):#Se comprueba la opcion enviada por la pagina
            estadoPuerto = '1'
            if gpio_disponible: #Si esta instalada la libreria RPi.GPIO se cambia el estado del puerto
                GPIO.output(nrp, GPIO.HIGH)
            else:#Si no esta instalada la libreria RPi.GPIO se muestra un mensaje
                print("No se puede activar el puerto: RPi.GPIO no instalado")
            
        else:
            estadoPuerto = '0'
            
            if gpio_disponible:#Si esta instalada la libreria RPi.GPIO se cambia el estado del puerto
                GPIO.output(nrp, GPIO.LOW)
            else:#Si no esta instalada la libreria RPi.GPIO se muestra un mensaje
                print("No se puede desactivar el puerto: RPi.GPIO no instalado")
            
            
        if(gpio_disponible):#Si esta instalada la libreria RPi.GPIO se cambia el estado del puerto
            estadoPuerto = str(GPIO.input(nrp))#Se lee el estado actual del puerto actual
        else:#Si no esta instalada la libreria RPi.GPIO se muestra un mensaje
            print("No se puede leer estado del puerto: RPi.GPIO no instalado")
        
        infoPuerto = {#Se crea el objeto JSON para enviar a la pagina
            "estadoActual": estadoPuerto,
            "puertoActual": nrp,
        }
        return HttpResponse(json.dumps(infoPuerto), content_type="application/json")#Se envia el objeto JSON
    else:#Ocurre si no se eviaron datos para un puerto
        return HttpResponseRedirect("/control/")

def acerca(request):
    return render(request, 'acerca.html')

def login (request):
    return render(request, "login.html")
        
    
def loginget(request): 
                if request.method == "POST":
                                    if request.POST.has_key('usuariof') and request.POST.has_key('passwordf'):
                                         x=request.POST.get('usuariof')
                                         y=request.POST.get('passwordf')
                                         try:
                                             usr = usuario.objects.get(usuario=x, password=y)                                             
                                             print("password:"+usr.password)
                                             print("usuario<<<<<"+usr.usuario)
                                             request.session['ses_usuario'] = usr.usuario
                                             request.session['ses_usuario_nivel'] = usr.nivel                            
                                             return HttpResponseRedirect("/control/")
                                         except ObjectDoesNotExist:
                                             print("Error de logueo")
                                             return render(request, 'login.html', {'mensaje':'Error de autenticación'}) 
                else:
                    print("No es Pos")
                    return render(request, 'login.html', {'mensaje':''})  
   
def cerrarses(request):
                try:
                    del request.session['ses_usuario']
                    del request.session['ses_usuario_nivel']
                except KeyError:
                    pass 
                    print("key error")
                return render(request, 'control.html',{'session':''})