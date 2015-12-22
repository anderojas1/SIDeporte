from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from Coldeportes.models import Entidad
from Coldeportes.grupos import InformacionUsuario
from django.contrib.auth import authenticate
from noticias.models import Noticias

class Index(TemplateView):
	template_name = 'startbootstrap/pages/inicio.html'

	def get_context_data(self, **kwargs):
		context = super(Index, self).get_context_data(**kwargs)

		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.asignarGrupo(self.request.user)
		context[grupo] = grupo
		print(grupo)
		#entidad = Entidad.objects.get(codigo=kwargs['id_entidad'])

		#if entidad.usuario == usuario:
		#	context['editable'] = True

		noticias = Noticias.objects.all()
		context['noticias'] = noticias

		return context