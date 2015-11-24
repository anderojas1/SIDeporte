from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Entidad
from .forms import FormRegistroEntidad

class DetallesEntidad(TemplateView):
	template_name = 'Entidades/detalles_entidad.html'
	entidad = None

	def get_context_data(self, **kwargs):
		context = super(DetallesEntidad, self).get_context_data(**kwargs)
		
		self.entidad = Entidad.objects.get(codigo = kwargs['id_entidad'])
		if 'entidad' not in context:
			context['entidad'] = self.entidad

		return context


class RegistrarEntidad(TemplateView):
	template_name = 'Entidades/registrar_entidad.html'
	form_registrar_noticia = FormRegistroEntidad()

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