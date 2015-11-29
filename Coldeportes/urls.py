from django.conf.urls import include, url, patterns
from django.contrib import admin

from .views import *


entidad_urls = patterns('',
	url(r'^(?P<id_entidad>\d+)/$', DetallesEntidad.as_view(), name='detalles_entidad'),
	url(r'^buscar$', BuscarEntidades.as_view(), name='detalles_entidad'),
	url(r'^registrar$', RegistrarEntidad.as_view(), name='registrar_entidad'),
)

deportistas_urls = patterns('',
	url(r'^(?P<id_deportista>\d+)/$', DetallesDeportistas.as_view(), name='detalles_deportistas'),
	url(r'^(?P<id_deportista>\d+)/delete$', BorrarDeportistas.as_view(), name='borrar_deportistas'),
	url(r'^buscar$', BuscarDeportistas.as_view(), name='buscar_deportistas'),
)

urlpatterns =  patterns ('',
    url(r'^entidad/', include(entidad_urls)),
    url(r'^deportistas/', include(deportistas_urls)),
    #url(r'^buscar$', BuscarNoticias.as_view(), name='buscar_noticias'),
    #url(r'^registrar$', RegistrarNoticia.as_view(), name='registrar_noticia'),
    #url(r'^(?P<id_noticias>\d+)/delete$', BorrarNoticia.as_view(), name='borrar_noticia'),
)
