from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Noticias
from .forms import FormRegistroNoticias
# Create your views here.


class DetallesNoticia(TemplateView):
	template_name = 'noticias/detalles_noticia.html'
	noticia = None

	def get_context_data(self, **kwargs):
		context = super(DetallesNoticia, self).get_context_data(**kwargs)
		print(kwargs['id_noticias'])

		self.noticia = Noticias.objects.get(pk=self.kwargs['id_noticias'])
		if 'noticia' not in context:
			context['noticia'] = self.noticia

		return context


class BuscarNoticias(TemplateView):
	template_name = 'noticias/buscar_noticias.html'
	noticias = []

	def get_context_data(self, **kwargs):
		context = super(BuscarNoticias, self).get_context_data(**kwargs)

		self.noticias = Noticias.objects.filter(estado=True)
		context['noticias'] = self.noticias

		return context


class RegistrarNoticia(TemplateView):
	template_name = 'noticias/registrar_noticia.html'
	form_registrar_noticia = FormRegistroNoticias()

	def get_context_data(self, **kwargs):
		context = super(RegistrarNoticia, self).get_context_data(**kwargs)

		context['form'] = self.form_registrar_noticia
		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarNoticia, self).get_context_data(**kwargs)
		self.form_registrar_noticia = FormRegistroNoticias(request.POST, request.FILES)

		if self.form_registrar_noticia.is_valid():
			print('es válido')
			self.form_registrar_noticia.save()
			context['exito'] = 'La noticia ha sido registrada exitosamente'

			return render(request, self.template_name, context)

		else:
			context['form'] = self.form_registrar_noticia
			return render(request, self.template_name, context)



class BorrarNoticia(TemplateView):
	template_name = 'noticias/borrar_noticia.html'

	def get_context_data(self, **kwargs):
		context = super(BorrarNoticia, self).get_context_data(**kwargs)

		noticia = Noticias.objects.get(codigo=kwargs['id_noticias'])
		context['noticia'] = noticia

		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarNoticia, self).get_context_data(**kwargs)

		noticia = Noticias.objects.get(codigo=kwargs['id_noticias'])
		noticia.estado = False
		noticia.save(update_fields=['estado'])
		context['borra_noticia'] = 'Se ha borrado la noticia exitosamente'

		return render(request, 'noticias/buscar_noticias.html', context)