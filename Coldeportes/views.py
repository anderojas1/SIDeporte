from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist

from .models import Entidad, Deportistas, Ubicacion, Dedicacion, DedicacionEntidad
from .forms import *
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
	form_ubicacion = FormRegistroUbicacion()

	def get_context_data(self, **kwargs):
		context = super(RegistrarEntidad, self).get_context_data(**kwargs)

		usuario = self.request.user
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.verGrupo(usuario)
		context[grupo] = grupo
		print(grupo)
		dedicacion = Dedicacion.objects.all()
		context['dedicaciones'] = dedicacion

		context['form_entidad'] = self.form_registrar_entidad
		context['form_dedicacion'] = self.form_registro_dedicacion
		context['form_ubicacion'] = self.form_ubicacion
		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarEntidad, self).get_context_data(**kwargs)
		self.form_registrar_entidad = FormRegistroEntidad(request.POST)
		self.form_registro_dedicacion = FormRegistroDedicacionEntidad(request.POST)
		self.form_ubicacion = FormRegistroUbicacion(request.POST)
		municipio = request.POST['municipio']
		departamento = request.POST['type']

		if self.form_registrar_entidad.is_valid() and self.form_registro_dedicacion.is_valid():
			nombre = self.form_registrar_entidad.cleaned_data['nombre']
			try:
				ubicacion = Ubicacion.objects.get(departamento=departamento, municipio=municipio)
				self.form_registrar_entidad.save()
				entidad = Entidad.objects.get(nombre=nombre)
				entidad.ubicacion = ubicacion
				entidad.save(update_fields=['ubicacion'])
				print(self.form_registro_dedicacion.cleaned_data)
				for dedicacion in self.form_registro_dedicacion.cleaned_data['escoger_dedicaciones']:
					ded = Dedicacion.objects.get(dedicacion=dedicacion)
					ded_ent = DedicacionEntidad(dedicacion=ded, entidad=entidad)
					ded_ent.save()
				context['exito'] = 'La entidad ha sido registrada exitosamente'
				return render(request, self.template_name, context)
			except ObjectDoesNotExist:
				return render(request, self.template_name, context)

		else:
			print(self.form_registrar_entidad.errors)
			print(self.form_registro_dedicacion.errors)
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

@csrf_exempt
def ajax_get_municipios(request):

	if request.is_ajax() and request.method=='POST':
		departamento = request.POST.get('type', '')
		municipios = Ubicacion.objects.filter(departamento=departamento).values_list('municipio', flat=True)

	return render_to_response('Entidades/buscar_municipios.html', locals())