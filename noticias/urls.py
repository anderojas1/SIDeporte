from django.conf.urls import include, url, patterns
from django.contrib import admin

from .views import DetallesNoticia

urlpatterns =  patterns ('',
    url(r'^(?P<id_noticias>\d+)/$', DetallesNoticia.as_view(), name='detalles_noticia'),
)