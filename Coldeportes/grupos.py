from django.contrib.auth.models import Group
from .models import Entidad

class InformacionUsuario():

	def buscarGrupo(self, usuario):
		id_grupo = usuario.groups.all()
		try:
			grupo = Group.objects.get(id=id_grupo).name
		except Group.DoesNotExist:
			grupo = 'invitado'
		return grupo

	def verGrupo(self, usuario):
		return self.buscarGrupo(usuario)

	def buscarEntidad(self, usuario):
		entidad = Entidad.objects.get(id_usuario=usuario.id)
		return entidad

	def asignarGrupo(self, usuario):
		ver_grupo = InformacionUsuario()
		grupo = ver_grupo.verGrupo(usuario)
		return grupo