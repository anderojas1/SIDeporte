from django.conf.urls import include, url, patterns
from django.contrib import admin

from .views import DetallesNoticia, BuscarNoticias, RegistrarNoticia

urlpatterns =  patterns ('',
    url(r'^(?P<id_noticias>\d+)/$', DetallesNoticia.as_view(), name='detalles_noticia'),
    url(r'^buscar$', BuscarNoticias.as_view(), name='buscar_noticias'),
    url(r'^registrar$', RegistrarNoticia.as_view(), name='registrar_noticia')
)