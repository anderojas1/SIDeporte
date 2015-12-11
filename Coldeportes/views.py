from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

from .models import Entidad, Deportistas, Ubicacion, Dedicacion, DedicacionEntidad
from .forms import *
from .grupos import InformacionUsuario
from .match_ubicacion import *


# VER LOS DETALLES DE UNA ENTIDAD
class DetallesEntidad(TemplateView):

	# TEMPLATE A USAR
	template_name = 'Entidades/detalles_entidad.html'
	entidad = None


	# CARGAR INFORMACIÓN PREVIA
	def get_context_data(self, **kwargs):
		context = super(DetallesEntidad, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo
		
		self.entidad = Entidad.objects.get(codigo = kwargs['id_entidad'])
		if 'entidad' not in context:
			context['entidad'] = self.entidad

		ubicacion = self.entidad.ubicacion
		if 'ubicacion' not in context:
			context['ubicacion'] = ubicacion

		dedicaciones = DedicacionEntidad.objects.filter(entidad_id=self.entidad.codigo)

		if 'dedicaciones' not in context:
			context['dedicaciones'] = dedicaciones

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
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo
		municipio = request.POST['municipio']
		departamento = request.POST['type']

		# SI LOS FORMULARIOS DE DEDICACIÓN Y REGISTRO DE ENTIDAD ESTÁN CORRECTOS
		if self.form_registrar_entidad.is_valid() and self.form_registro_dedicacion.is_valid():
			nombre = self.form_registrar_entidad.cleaned_data['nombre']
			try:

				# BUSCAR EN LA BD SI EL DEPARTAMENTO Y MUNICIPIO EXISTEN
				ubicacion = Ubicacion.objects.get(departamento=departamento, municipio=municipio)

				# REGISTRO DE LA ENTIDAD
				self.form_registrar_entidad.save()
				entidad = Entidad.objects.get(nombre=nombre)

				# ASIGNACIÓN DE UBICACIÓN
				entidad.ubicacion = ubicacion
				entidad.save(update_fields=['ubicacion'])

				# REGISTRO DE DEDICACIONES (TANTAS COMO HAYA SELECCIONADO)
				for dedicacion in self.form_registro_dedicacion.cleaned_data['escoger_dedicaciones']:
					ded = Dedicacion.objects.get(dedicacion=dedicacion)
					ded_ent = DedicacionEntidad(dedicacion=ded, entidad=entidad)
					ded_ent.save()

				# CREACIÓN DE USUARIO EN LA BASE DE DATOS
				usuario = User.objects.create_user(username=entidad.correo, password=str(entidad.cc_representante_legal))
				entidad.usuario = usuario
				entidad.save(update_fields=['usuario'])

				# ASIGNACIÓN DE GRUPO EN LA BASE DE DATOS
				grupo = Group.objects.get(name='entidad')
				usuario.groups.add(grupo)

				context['exito'] = 'La entidad ha sido registrada exitosamente'
				return render(request, self.template_name, context)
			except ObjectDoesNotExist:

				# SI NO EXISTE LA UBICACIÓN
				return render(request, self.template_name, context)

		else:
			print(self.form_registrar_entidad.errors)
			print(self.form_registro_dedicacion.errors)
			return render(request, self.template_name, context)

class BorrarEntidad(TemplateView):
	template_name = 'Entidades/borrar_entidad.html'

	def get_context_data(self, **kwargs):
		context = super(BorrarEntidad, self).get_context_data(**kwargs)

		entidad = Entidad.objects.get(codigo=kwargs['id_entidad'])
		context['entidad'] = entidad

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarEntidad, self).get_context_data(**kwargs)

		entidad = Entidad.objects.get(codigo=kwargs['id_entidad'])
		entidad.estado = False
		entidad.save(update_fields=['estado'])
		context['borra_entidad'] = 'Se ha borrado la entidad exitosamente'

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return render(request, 'Entidades/buscar_entidades.html', context)

class EditarEntidad(TemplateView):
	template_name = 'Entidades/editar_entidad.html'
	
	def get_context_data(self, **kwargs):
		context = super(EditarEntidad, self).get_context_data(**kwargs)

		# CARGAR INFORMACIÓN DE USUARIO ACTUAL
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		# CARGAR ENTIDAD ASOCIADA
		entidad = Entidad.objects.get(codigo=kwargs['id_entidad'])

		# CARGAR DEDICACIONES DE LA ENTIDAD
		dedicaciones_entidad = DedicacionEntidad.objects.filter(entidad_id=entidad.codigo).values('dedicacion_id')
		dedicaciones = Dedicacion.objects.filter(id__in=dedicaciones_entidad)

		context['entidad'] = entidad
		context[str(entidad.tipo)+'t'] = entidad.tipo
		context[str(entidad.caracter_economico)+'c'] = entidad.caracter_economico

		for dedicacion in dedicaciones:
			context[str(dedicacion.id)+'d'] = dedicacion.id

		departamentos = Ubicacion.objects.all().distinct('departamento').values('departamento')
		departamento_sel = entidad.ubicacion.departamento
		municipios = Ubicacion.objects.filter(departamento=departamento_sel).values('municipio')
		municipio_sel = entidad.ubicacion.municipio
		datos_ubicacion = match_municipio_departamento(municipio_sel, departamento_sel, municipios, departamentos)
		context['datos_ubicacion'] = datos_ubicacion

		#print(context)

		return context

	def post(self, request, *args, **kwargs):
		context = super(EditarEntidad, self).get_context_data(**kwargs)

		print (request.POST)

		# CODIGO EN BASE DE DATOS
		entidad = Entidad.objects.get(codigo=kwargs['id_entidad'])

		# CAMPOS EDITABLES
		entidad.nombre = request.POST['nombre']
		entidad.tipo = request.POST['tipo']
		entidad.caracter_economico = request.POST['caracter_economico']
		entidad.telefono = request.POST['telefono']
		entidad.correo = request.POST['correo']
		entidad.direccion = request.POST['direccion']
		entidad.cc_representante_legal = request.POST['cc_representante_legal']
		entidad.nombre_representante_legal = request.POST['nombre_representante_legal']

		entidad.save(update_fields=['nombre', 'tipo', 'caracter_economico', 'telefono', 'direccion', 'correo', 'cc_representante_legal', 'nombre_representante_legal'])

		kwargs['edicion'] = 'Se han modificado los datos exitosamente'

		return redirect ("/coldeportes/entidad/" + kwargs['id_entidad'], **kwargs)


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