from django.conf.urls import patterns, include, url
from django.contrib import admin
from control.views import control, accionarControl, acerca, users
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^control/$', control),
    url(r'^accionarControl/$', accionarControl),
    url(r'^acerca/$', acerca),
    url(r'^usuarios/$', users),
    # Examples:
    # url(r'^$', 'OgaKatupyry.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
