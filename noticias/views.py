from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView

from .models import Noticias
from .forms import FormRegistroNoticias, FormEdicionNoticias
from Coldeportes.grupos import InformacionUsuario
# Create your views here.


class DetallesNoticia(TemplateView):
	template_name = 'noticias/detalles_noticia.html'
	noticia = None

	def get_context_data(self, **kwargs):
		context = super(DetallesNoticia, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		self.noticia = Noticias.objects.get(pk=self.kwargs['id_noticias'])
		if 'noticia' not in context:
			context['noticia'] = self.noticia

		return context

	"""def post(self, request, *args, **kwargs):
		context = super(DetallesNoticia, self).get_context_data(**kwargs)

		
		return redirect("update", "algo")"""


class BuscarNoticias(TemplateView):
	template_name = 'noticias/buscar_noticias.html'
	noticias = []

	def get_context_data(self, **kwargs):
		context = super(BuscarNoticias, self).get_context_data(**kwargs)

		self.noticias = Noticias.objects.filter(estado=True)
		context['noticias'] = self.noticias

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context


class RegistrarNoticia(TemplateView):
	template_name = 'noticias/registrar_noticia.html'
	form_registrar_noticia = FormRegistroNoticias()

	def get_context_data(self, **kwargs):
		context = super(RegistrarNoticia, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.form_registrar_noticia
		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarNoticia, self).get_context_data(**kwargs)
		self.form_registrar_noticia = FormRegistroNoticias(request.POST, request.FILES)

		if self.form_registrar_noticia.is_valid():
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

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarNoticia, self).get_context_data(**kwargs)

		noticia = Noticias.objects.get(codigo=kwargs['id_noticias'])
		noticia.estado = False
		noticia.save(update_fields=['estado'])
		context['borra_noticia'] = 'Se ha borrado la noticia exitosamente'

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return render(request, 'noticias/buscar_noticias.html', context)

class EditarNoticia (TemplateView):
	model = Noticias
	template_name = 'noticias/editar_noticias.html'
	fields = ['titulo', 'contenido']

	def get_context_data(self, **kwargs):
		context = super(EditarNoticia, self).get_context_data(**kwargs)
		#context['form'] = self.form
		#print(kwargs)
		noticia = Noticias.objects.get(codigo=kwargs['id_noticias'])
		context['noticia'] = noticia

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		context = super(EditarNoticia, self).get_context_data(**kwargs)
		noticia = Noticias.objects.get(codigo=kwargs['id_noticias'])
		if 'noticia' not in context:
			context['noticia'] = noticia

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		form = FormEdicionNoticias(request.POST, request.FILES)

		if form.is_valid():
			if (form.cleaned_data['imagen'] is not None):
				imagen = form.cleaned_data['imagen']	
				noticia.imagen = imagen
				noticia.save(update_fields=['imagen'])
			titulo = form.cleaned_data['titulo']
			contenido = form.cleaned_data['contenido']
			noticia.titulo = titulo
			noticia.contenido = contenido
			noticia.save(update_fields=['titulo'])
			noticia.save(update_fields=['contenido'])
			context['edit_not'] = "La noticia \"" + noticia.titulo + "\" ha sido actualizada exitosamente"
		else:
			print(self.form.errors)
		return render(request, "noticias/detalles_noticia.html", context)