from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Entidad, Deportistas, Ubicacion, Dedicacion
from .forms import FormRegistroEntidad, FormRegistroDedicacionEntidad
from .grupos import InformacionUsuario

class DetallesEntidad(TemplateView):
	template_name = 'Entidades/detalles_entidad.html'
	entidad = None

	def get_context_data(self, **kwargs):
		context = super(DetallesEntidad, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo
		
		self.entidad = Entidad.objects.get(codigo = kwargs['id_entidad'])
		if 'entidad' not in context:
			context['entidad'] = self.entidad

		return context

class RegistrarEntidad(TemplateView):
	template_name = 'Entidades/registrar_entidad.html'
	form_registrar_entidad = FormRegistroEntidad()
	form_registro_dedicacion = FormRegistroDedicacionEntidad()

	def get_context_data(self, **kwargs):
		context = super(RegistrarEntidad, self).get_context_data(**kwargs)

		usuario = self.request.user
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.verGrupo(usuario)
		context[grupo] = grupo
		print(grupo)
		dedicacion = Dedicacion.objects.all()
		context['dedicaciones'] = dedicacion
		print(dedicacion)

		context['form_entidad'] = self.form_registrar_entidad
		context['form_dedicacion'] = self.form_registro_dedicacion
		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarNoticia, self).get_context_data(**kwargs)
		self.form_registrar_entidad = FormRegistroNoticias(request.POST)

		if self.form_registrar_entidad.is_valid():
			print('es válido')
			self.form_registrar_entidad.save()
			context['exito'] = 'La noticia ha sido registrada exitosamente'

			ver_grupo = InformacionUsuario()
			grupo = ver_grupo.asignarGrupo(self.request.user)
			context[grupo] = grupo

			return render(request, self.template_name, context)

		else:
			context['form'] = self.form_registrar_noticia
			return render(request, self.template_name, context)

class UbicacionEntidades(TemplateView):
	template_name = 'Entidades/ubicacion_entidades.html'

	def get_context_data(self, **kwargs):
		context = super(UbicacionEntidades, self).get_context_data(**kwargs)

		usuario = self.request.user
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.verGrupo(usuario)
		context[grupo] = grupo

		return context

class DetallesDeportistas(TemplateView):
	template_name = 'Deportistas/detalles_deportista.html'
	entidad = None

	def get_context_data(self, **kwargs):
		context = super(DetallesDeportistas, self).get_context_data(**kwargs)
		
		self.deportista = Deportistas.objects.get(doc_identidad = kwargs['id_deportista'])
		if 'deportistas' not in context:
			context['deportistas'] = self.deportista
		return context

class BuscarEntidades(TemplateView):
	template_name = 'Entidades/buscar_entidades.html'
	entidades = []

	def get_context_data(self, **kwargs):
		context = super(BuscarEntidades, self).get_context_data(**kwargs)

		self.entidades = Entidad.objects.filter(estado=True)
		context['entidades'] = self.entidades

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

class BorrarDeportistas(TemplateView):
	template_name = 'Deportistas/borrar_deportista.html'

	def get_context_data(self, **kwargs):
		context = super(BorrarDeportistas, self).get_context_data(**kwargs)

		deportistas = Deportistas.objects.get(doc_identidad=kwargs['id_deportista'])
		context['deportistas'] = deportistas
		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarDeportistas, self).get_context_data(**kwargs)

		deportistas = Deportistas.objects.get(doc_identidad=kwargs['id_deportista'])
		deportistas.estado = False
		deportistas.save(update_fields=['estado'])
		context['borra_deportistas'] = 'Se ha borrado al deportista exitosamente'

		return render(request, 'coldeportes/deportistas/buscar_deportista.html', context)


class BuscarDeportistas(TemplateView):
	template_name = 'Deportistas/buscar_deportista.html'
	deportistas = []

	def get_context_data(self, **kwargs):
		context = super(BuscarDeportistas, self).get_context_data(**kwargs)

		self.deportistas = Deportistas.objects.filter(estado=True)
		context['deportistas'] = self.deportistas
		print (self.deportistas)

		return context