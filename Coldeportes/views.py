from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
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

				# CAPTACIÓN DE LA CONTRASEÑA DE ACCESO

				password_1 = request.POST['password_1']
				password_2 = request.POST['password_2']

				if password_2 == password_1 and len(password_1) > 0:

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

					usuario = User.objects.create_user(username=entidad.codigo, password=password_1)
					entidad.usuario = usuario
					entidad.save(update_fields=['usuario'])

					# ASIGNACIÓN DE GRUPO EN LA BASE DE DATOS
					grupo = Group.objects.get(name='entidad')
					usuario.groups.add(grupo)

					context['exito'] = 'La entidad ha sido registrada exitosamente'
					return render(request, self.template_name, context)

				else:
					print("son nulos o no coinciden")
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
		lista_departamentos = []
		for departamento in departamentos:
			lista_departamentos.append(departamento['departamento'])
		departamento_sel = entidad.ubicacion.departamento
		municipios = Ubicacion.objects.filter(departamento=departamento_sel).values('municipio')
		municipio_sel = entidad.ubicacion.municipio
		context['datos_departamento'] = lista_departamentos
		context['datos_municipios'] = municipios
		context['dep_sel'] = departamento_sel
		context['mun_sel'] = municipio_sel

		#print(context)

		return context

	def post(self, request, *args, **kwargs):
		context = super(EditarEntidad, self).get_context_data(**kwargs)

		# CARGAR INFORMACIÓN DE USUARIO ACTUAL
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

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
	deportistas = []

	def get_context_data(self, **kwargs):
		context = super(BuscarEntidades, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		if grupo == 'coldeportes':
			pass

		else:

			entidad = Entidad.objects.get(usuario=self.request.user)

			self.deportistas = Deportistas.objects.filter(estado=True, entidad=entidad)
			context['deportistas'] = self.deportistas
		
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

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		self.deportistas = Deportistas.objects.filter(estado=True)
		context['deportistas'] = self.deportistas
		print (self.deportistas)

		return context

class RegistrarDeportista(TemplateView):
	template_name = 'Deportistas/registrar_deportista.html'
	form_deportista = FormRegistroDeportista()

	def get_context_data(self, **kwargs):
		context = super(RegistrarDeportista, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.form_deportista

		return context


class RegistrarEscenario(TemplateView):
	template_name = 'escenarios/registrar_escenario.html'
	form_escenario = FormRegistrarEscenario()
	form_ubicacion = FormRegistroUbicacion()

	def get_context_data(self, **kwargs):
		context = super(RegistrarEscenario, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		dedicaciones = Dedicacion.objects.all()

		context['form'] = self.form_escenario
		context['dedicaciones'] = dedicaciones
		context['form_ubicacion'] = self.form_ubicacion

		return context


	def post(self, request, *args, **kwargs):
		context = super(RegistrarEscenario, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		self.form_escenario = FormRegistrarEscenario(request.POST)
		municipio = request.POST['municipio']
		departamento = request.POST['type']

		if self.form_escenario.is_valid():
			try:

				# BUSCAR EN LA BD SI EL DEPARTAMENTO Y MUNICIPIO EXISTEN
				ubicacion = Ubicacion.objects.get(departamento=departamento, municipio=municipio)

				if grupo == 'coldeportes':
					pass

				else:
					entidad = Entidad.objects.get(usuario=self.request.user)

					print(request.POST)

					nombre = request.POST['nombre']
					direccion = request.POST['direccion']
					actividad = request.POST['actividad']
					descripcion = request.POST['descripcion']

					dedicacion = Dedicacion.objects.get(id=request.POST['dedicacion'])

					capacidad_e = request.POST['capacidad_publico']
					capacidad_d = request.POST['capacidad_deportistas']
					escala = request.POST['escala']

					escenario = Escenarios(nombre=nombre, direccion=direccion, actividad=actividad, 
						descripcion=descripcion, tipo=dedicacion, capacidad_publico=capacidad_e, 
						capacidad_deportistas=capacidad_d, escala=escala, entidad=entidad)

					escenario.save()

					escenario.ubicacion = ubicacion
					escenario.save(update_fields=['ubicacion'])

					context['exito_escenario_nombre'] = 'el escenario ' + nombre

				context['exito_escenario'] = ' ha sido registrado el escenario exitosamente'

				return render (request, self.template_name, context)

			# SI NO EXISTE EL DEPARTAMENTO Y EL MUNICIPIO
			except ObjectDoesNotExist:

				# CARGAR NUEVAMENTE LOS FORMULARIOS
				self.form_escenario = FormRegistrarEscenario()
				self.form_ubicacion = FormRegistroUbicacion()
				context['form'] = self.form_escenario
				context['form_ubicacion'] = self.form_ubicacion

				# CARGAR INFORMACIÓN DEL ERROR
				context['error_ubicacion'] = 'Por favor seleccione un departamento y un municipio válidos'

				dedicaciones = Dedicacion.objects.all()
				context['dedicaciones'] = dedicaciones

				return render(request, self.template_name, context)

		# SI EL FORMULARIO NO ESTÁ COMPLETO
		else:

			# CARGAR NUEVAMENTE LOS FORMULARIOS
			self.form_escenario = FormRegistrarEscenario()
			self.form_ubicacion = FormRegistroUbicacion()
			context['form'] = self.form_escenario
			context['form_ubicacion'] = self.form_ubicacion

			# CARGAR INFORMACIÓN DEL ERROR
			context['error'] = 'Todos los campos son requeridos'

			dedicaciones = Dedicacion.objects.all()
			context['dedicaciones'] = dedicaciones

			return render(request, self.template_name, context)


class DetallesEscenario(TemplateView):
	template_name = "escenarios/detalles_escenario.html"

	def get_context_data(self, **kwargs):
		context = super(DetallesEscenario, self).get_context_data(**kwargs)
		print(kwargs)

		# CARGAR DATOS DE ESCENARIO
		escenario = Escenarios.objects.get(codigo=kwargs['id_escenario'])
		context['escenario'] = escenario

		# CARGAR INFORMACIÓN DE USUARIO
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		entidad_consulta = Entidad.objects.get(usuario=self.request.user)

		if escenario.entidad == entidad_consulta:
			context['puede_editar'] = True

		current_url = self.request.resolver_match.url_name
		print(current_url)

		if current_url.find('success'):
			context['editado'] = 'Se han actualizado exitosamente los datos del escenario: ' + escenario.nombre

		return context

class BorrarEscenario(TemplateView):
	template_name = 'escenarios/borrar_escenario.html'

	def get_context_data(self, **kwargs):
		context = super(BorrarEscenario, self).get_context_data(**kwargs)

		escenario = Escenarios.objects.get(codigo=kwargs['id_escenario'])
		context['escenario'] = escenario

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarEscenario, self).get_context_data(**kwargs)

		escenario = Escenarios.objects.get(codigo=kwargs['id_escenario'])
		escenario.estado = False
		escenario.save(update_fields=['estado'])
		context['borra_escenario'] = 'Se ha borrado el escenario exitosamente'

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return render(request, 'escenarios/buscar_escenarios.html', context)

class EditarEscenario(TemplateView):
	template_name = 'escenarios/editar_escenario.html'

	def cargar_informacion(self, context, escenario):

		# CARGAR ESCALA NUMÉRICA DE CALIFICACIÓN DEL ESTADO DEL ESCENARIO
		listado_escala = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		context['listado_escala'] = listado_escala

		# CARGAR TIPO DE ACTIVIDAD
		dedicaciones = Dedicacion.objects.all()
		context['dedicaciones'] = dedicaciones

		# CARGAR DEPARTAMENTOS
		departamentos = Ubicacion.objects.all().distinct('departamento').values('departamento')
		context['departamentos'] = departamentos

		# CARGAR MUNICIPIOS
		municipios = Ubicacion.objects.filter(departamento=escenario.ubicacion.departamento).values('municipio')
		context['municipios'] = municipios

	def get_context_data(self, **kwargs):
		context = super(EditarEscenario, self).get_context_data(**kwargs)

		# CARGAR INFORMACIÓN DEL ESCENARIO
		escenario = Escenarios.objects.get(codigo=kwargs['id_escenario'])
		context['escenario'] = escenario

		self.cargar_informacion(context, escenario)

		# CARGAR INFORMACIÓN DE USUARIO ACTUAL
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		context = super(EditarEscenario, self).get_context_data(**kwargs)

		# CARGAR INFORMACIÓN DE USUARIO ACTUAL
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo

		escenario = Escenarios.objects.get(codigo=kwargs['id_escenario'])
		context['escenario'] = escenario

		departamento = request.POST['type']
		municipio = request.POST['municipio']

		try:

			# OBTENER LA UBICACIÓN
			ubicacion = Ubicacion.objects.get(departamento=departamento, municipio=municipio)

			# OBTENER TODOS LOS CAMPOS EDITABLES
			nombre = request.POST['nombre']
			direccion = request.POST['direccion']
			actividad = request.POST['actividad']
			capacidad_e = request.POST['capacidad_publico']
			descripcion = request.POST['descripcion']
			capacidad_d = request.POST['capacidad_deportistas']
			escala = request.POST['escala']
			dedicacion = Dedicacion.objects.get(id=request.POST['dedicacion'])

			# SI FALTA ALGUNA INFORMACIÓN: CAMPOS VACÍOS
			if not nombre or not direccion or not actividad or not capacidad_d or not capacidad_e or not descripcion:
				
				pass

			else:

				escenario.nombre = nombre
				escenario.direccion = direccion
				escenario.actividad = actividad
				escenario.capacidad_publico = capacidad_e
				escenario.capacidad_deportistas = capacidad_d
				escenario.descripcion = descripcion
				escenario.escala = escala
				escenario.tipo = dedicacion
				escenario.ubicacion = ubicacion

				escenario.save(update_fields=['nombre', 'direccion', 'actividad', 'capacidad_publico', 'ubicacion',
					'capacidad_deportistas', 'descripcion', 'escala', 'tipo'])

				edit = 'Se han actualizado exitosamente los datos del escenario: ' + escenario.nombre

				return redirect("/coldeportes/escenarios/" + kwargs['id_escenario'] + '/update/success',
					edit)

		except ObjectDoesNotExist:
			context['error'] = 'Por favor ingrese un mmunicipio y departamento válidos'

			self.cargar_informacion(context, escenario)

			return render(request, self.template_name, context)


		return render(request, self.template_name, context)


@csrf_exempt
def ajax_get_municipios(request):

	if request.is_ajax() and request.method=='POST':
		departamento = request.POST.get('type', '')
		municipios = Ubicacion.objects.filter(departamento=departamento).values_list('municipio', flat=True)

	return render_to_response('Entidades/buscar_municipios.html', locals())