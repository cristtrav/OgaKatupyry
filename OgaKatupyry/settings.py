"""
Django settings for OgaKatupyry project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
try:
    import RPi.GPIO as GPIO
    gpio_disponible = True
except ImportError:
    gpio_disponible = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Definicion de carpetas donde estaran los archivos estaticos
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'control','css'),
    os.path.join(BASE_DIR,'control','js'),
    os.path.join(BASE_DIR,'control','imagenes'),
)

# Definicion de carpetas donde estaran las plantillas HTML
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'control','plantillas'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ge73e1s_yx%iiq+i76tkk%xhh2@j-jcfry0y0qwh%vph^y+ge='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'control',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OgaKatupyry.urls'

WSGI_APPLICATION = 'OgaKatupyry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#DESCOMENTAR LAS SIGUEIENTES LINEAS CUANDO SE DESPLIEGA EN EL RASPBERRY CONTANDO CON LA LIBRERIA RPi.GPIO
from control.models import configPuerto#Importo el modelo de configuracion de puertos para habilitar
from django.db import OperationalError#Importada libreria de base dedatos de django
if gpio_disponible:#Compruebo si la libreria RPi.GPIO esta instalada
    
    print("RPi.GPIO instalado")
    GPIO.setmode(GPIO.BOARD)#Establezco el modo de numeracion de los puertos
    GPIO.setwarnings(False)#Deshabilitar las advertencias
    try:#Comprobar si existe la base de datos o la tabla
        pts = configPuerto.objects.all()#Obtener los puertos configurados en la base de datos
        for p in pts:#Iterar el resultado de la consulta
            GPIO.setup(p.puertoon, GPIO.OUT)# se establece el puerto de encendido como salida
            GPIO.setup(p.puertooff, GPIO.OUT)# se establece el puerto de apagado como salida
            GPIO.output(p.puertoon, GPIO.HIGH)# EL puerto estara en reposo en ALTO
            GPIO.output(p.puertooff, GPIO.HIGH)# EL puerto estara en reposo en ALTO
    except OperationalError:
        print ("Tabla o base de datos no encontrada")
else:#Si la libreria RPi.GPIO no esta instalada muestro un mensaje
    print("RPi.GPIO No instalado")
