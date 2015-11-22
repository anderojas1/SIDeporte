from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Noticias
# Create your views here.


class DetallesNoticia(TemplateView):
	template_name = 'noticias/detalles_noticia.html'
	noticia = None

	def get_context_data(self, **kwargs):
		context = super(DetallesNoticia, self).get_context_data(**kwargs)

		self.noticia = Noticias.objects.get(pk=self.kwargs['id_noticias'])
		if 'noticia' not in context:
			context['noticia'] = self.noticia

		return context


class BuscarNoticias(TemplateView):
	template_name = 'noticias/buscar_noticias.html'
	noticias = []

	def get_context_data(self, **kwargs):
		context = super(BuscarNoticias, self).get_context_data(**kwargs)

		self.noticias = Noticias.objects.all()
		context['noticias'] = self.noticias
		print(context['noticias'][0].imagen.url)

		return context