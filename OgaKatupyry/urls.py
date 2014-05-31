from django.conf.urls import patterns, include, url
from django.contrib import admin
from control.views import control, accionarControl, acerca, loginget, cerrarses, users, editUsers, newUsers, processUser, eliminarUser, savePuertos, configuracion, update, deleteall


#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^control/$', control),
    url(r'^accionarControl/$', accionarControl),
    url(r'^acerca/$', acerca),
    url(r'^login/$', loginget),
    url(r'^cerrarses/$', cerrarses),
    url(r'^usuarios/$', users),
    url(r'^usuarios/editar/$', newUsers),
    url(r'^usuarios/editar/([0-9]+)/$', editUsers),
    url(r'^usuarios/eliminar/([0-9]+)/$', eliminarUser),
    url(r'^usuarios/procesar/$', processUser),
    url(r'^savePuertos/$', savePuertos),
    url(r'CRUD/$', CRUD),
    url(r'^Configuracion/$', configuracion),
    url(r'^update/$', update),
    url(r'^deleteall/$', deleteall),
    # Examples:
    #string parameter: (?P<accion>[\w\-]+)
    # url(r'^$', 'OgaKatupyry.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
