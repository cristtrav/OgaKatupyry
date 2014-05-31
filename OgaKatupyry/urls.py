from django.conf.urls import patterns, include, url
from django.contrib import admin
from control.views import control, accionarControl, savePuertos, configuracion, update, deleteall
from control.CRUD import  CRUD
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^control/$', control),
    url(r'^accionarControl', accionarControl),
    url(r'^savePuertos/$', savePuertos),
    url(r'CRUD/$', CRUD),
    url(r'^Configuracion/$', configuracion),
    url(r'^update/$', update),
    url(r'^deleteall/$', deleteall),
    # Examples:
    # url(r'^$', 'OgaKatupyry.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   url(r'^admin/', include(admin.site.urls)),
    
)
