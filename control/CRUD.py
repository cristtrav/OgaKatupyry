from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from models import configPuerto
from django.shortcuts import render_to_response
from django.db.utils import OperationalError
try:
    import RPi.GPIO
    gpio_disponible = True
except ImportError:
    gpio_disponible = False

####################################Insert######################################################################
def savePuertos(request):
    bart = configPuerto.objects.all()
    return render(request, "savePuertos.html", {"opciones" : bart})
def CRUD(request):
            if request.POST.has_key('puertoon') and request.POST.has_key('puertoof') and request.POST.has_key('descripcion'):
                puertoon = request.POST.get('puertoon', 'nada')
                puertoof = request.POST.get('puertoof', 'nada')
                descripcion = request.POST.get('descripcion')
                print ("numero de puerto a ecender es" + puertoon)
                print ("numero de puerto a apagar es" + puertoof)
                print ("decripcion de puertos" + descripcion)     
                if configPuerto.objects.filter(puertoon = puertoon):
                    bart = configPuerto.objects.filter(puertoon = puertoon)
                    print ("p1")
                    return render(request, "savePuertos.html", {"opciones" : bart,'mesage':'Puerto ON ya estan en uso'} )
                elif configPuerto.objects.filter(puertooff = puertoon):
                    bart = configPuerto.objects.filter(puertoon = puertoon)
                    print ("p2")
                    return render(request, 'savePuertos.html', {"opciones" : bart,'mesage' : 'El puerto ya esta en uso'})
                elif configPuerto.objects.filter(puertooff = puertoof):
                    bart = configPuerto.objects.all()
                    return render (request, 'savePuertos.html', {"opciones" : bart,'mesage' : 'El puerto ya esta en uso'})
                elif configPuerto.objects.filter(descripcion = descripcion):
                    bart = configPuerto.objects.all()
                    print ("p3")
                    return render(request, 'savePuertos.html', { "opciones" : bart, 'mesage': 'la descripcion ya existe'})
                elif configPuerto.objects.filter(puertooff = puertoon):
                    bart = configPuerto.objects.all()
                    print("p4")
                    return render(request, 'savePuertos.html', {"opciones" : bart, 'mesage' : 'Los puertos no pueden coincidir'})
                elif(descripcion == ''):
                    bart = configPuerto.objects.all()
                    print("p5"  )
                    return render(request, 'savePuertos.html', {"opciones" : bart, 'mesage' : 'La descripcion esta vacia'})
                elif (puertoon == puertoof):
                    bart = configPuerto.objects.all()
                    print ("p6")
                    return render (request, 'savePuertos.html', {"opciones": bart, 'mesage' : 'Los puertos no pueden coincidir'})
                else:
                    cfg_puertos = configPuerto(puertoon = puertoon, puertooff = puertoof,  descripcion = descripcion)
                    cfg_puertos.save()
                    return HttpResponseRedirect('/Configuracion/')
            
            ###############################Delete####################################################################
            elif request.POST.has_key('idpuerto'):
                 idpuerto = request.POST.get('idpuerto')
                 delete = request.POST.get('eliminar')
                 print ("numero de puerto" + idpuerto)
                 if (idpuerto == ''):
                    return render(request, ('Configuracion.html', {'mesage' : 'Debes seleccionar el una casilla'}))
                 else:
                    cfg_puertos = configPuerto.objects.get(id = idpuerto)
                    cfg_puertos.delete()
                    if gpio_disponible:
                        print("RPi.GPIO instalado")
                        GPIO.setmode(GPIO.BOARD)
                        GPIO.setwarnings(false)
                        try:
                            GPIO.setup(cfg_puertos.puertoon, GPIO.OUT)
                            GPIO.setup(cfg_puertos.puertoof, GPIO.OUT)
                            GPIO.output(cfg_puertos.puertoon, GPIO.HIGH)
                            GPIO.output(cfg_puertos.puertoof, GPIO.HIGH)
                        except OperationalError:
                            print("no se ha encontrado db")
                    else:
                         print("RPi.GPIO no instalado")       
                    return HttpResponseRedirect('/Configuracion/')
            
            ################################UPDATE#########################################################################
            else:
                    if request.POST.has_key("nropuerto") and request.POST.has_key("descripcion"): 
                        puerto = request.POST.get("nropuerto")
                        newdts = request.POST.get("descripcion")
                        print ("la descripcion actual es:" + puerto)
                        print ("la nueva descripcion es " + newdts)
                        if configPuerto.objects.filter(descripcion = newdts):
                            return render (request, 'update.html', {'mesage' : 'la descripcion ya existe' })
                        else:
                            cfg_puertos = configPuerto.objects.filter(id = puerto).first()
                            print ("kjhk,jhklj" +str(cfg_puertos.id))
                            puertoenc = cfg_puertos.puertoon
                            puertoapag = cfg_puertos.puertooff
                            cfg_puertos = configPuerto(id = puerto, puertoon = puertoenc, puertooff = puertoapag, descripcion = newdts )
                            cfg_puertos.save()
                            return HttpResponseRedirect('/Configuracion/')