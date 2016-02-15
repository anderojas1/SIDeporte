from django.conf.urls import include, url, patterns
from django.contrib import admin

from .views import *


entidad_urls = patterns('',
	url(r'^(?P<id_entidad>\w+)/$', DetallesEntidad.as_view(), name='detalles_entidad'),
	url(r'^buscar$', BuscarEntidades.as_view(), name='buscar_entidades'),
	url(r'^registrar$', RegistrarEntidad.as_view(), name='registrar_entidad'),
	url(r'^ubicacion$', UbicacionEntidades.as_view(), name='ubicacion_entidades'),
	url(r'^(?P<id_entidad>\w+)/delete$', BorrarEntidad.as_view(), name='borrar_entidad'),
	url(r'^(?P<id_entidad>\w+)/update$', EditarEntidad.as_view(), name='borrar_entidad'),
	url(r'^buscarmunicipios$', ajax_get_municipios, name='ajax_get_municipios'),
)

deportistas_urls = patterns('',
	url(r'^(?P<id_deportista>\d+)/$', DetallesDeportistas.as_view(), name='detalles_deportistas'),
	url(r'^(?P<id_deportista>\d+)/delete$', BorrarDeportistas.as_view(), name='borrar_deportistas'),
	url(r'^buscar$', BuscarDeportistas.as_view(), name='buscar_deportistas'),
	url(r'^registrar$', RegistrarDeportista.as_view(), name='registrar_deportista'),
	url(r'^(?P<id_deportista>\w+)/update$', EditarDeportista.as_view(), name='editar_deportista'),
)

escenarios_urls = patterns ('',
	url(r'^registrar$', RegistrarEscenario.as_view(), name='registrar_escenario'),
	url(r'^listar$', ListarEscenarios.as_view(), name='listar_escenarios'),
	url(r'^(?P<id_escenario>\w+)/$', DetallesEscenario.as_view(), name='detalles_escenario'),
	url(r'^(?P<id_escenario>\w+)/delete$', BorrarEscenario.as_view(), name='borrar_escenario'),
	url(r'^(?P<id_escenario>\w+)/update$', EditarEscenario.as_view(), name='editar_escenario'),
	url(r'^(?P<id_escenario>\w+)/update/success$', DetallesEscenario.as_view(), name='editado_escenario'),
)

urlpatterns =  patterns ('',
    url(r'^entidad/', include(entidad_urls)),
    url(r'^deportistas/', include(deportistas_urls)),
    url(r'^escenarios/', include(escenarios_urls)),
    url(r'^buscaractividades$', ajax_get_actividades, name='ajax_get_actividades'),
    url(r'^quienes-somos$', QuienesSomos.as_view(), name='quienes-somos'),
    url(r'^mision-vision$', MisionVision.as_view(), name='mision-vision'),
    #url(r'^buscar$', BuscarNoticias.as_view(), name='buscar_noticias'),
    #url(r'^registrar$', RegistrarNoticia.as_view(), name='registrar_noticia'),
    #url(r'^(?P<id_noticias>\d+)/delete$', BorrarNoticia.as_view(), name='borrar_noticia'),
)
