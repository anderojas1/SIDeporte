from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Create your models here.


class Ubicacion(models.Model):
	codigo 		= models.AutoField(primary_key=True)
	departamento= models.CharField(max_length=30)	
	municipio 	= models.CharField(max_length=100)

	def __int__(self):
		return self.codigo

	def __str__(self):
		return self.municipio + "," + self.departamento
		
	def get_ubicacion(self):
		return departamento + ", " + municipio

class Dedicacion(models.Model):
	id = models.AutoField(primary_key=True)
	dedicacion = models.CharField(max_length=50)

	def __str__(self):
		return self.dedicacion
		

class Entidad(models.Model):

	codigo						= models.CharField(max_length=30, primary_key=True)
	nombre 						= models.CharField(max_length=30)
	opt_tipo					= ((0, 'Rector'), (1, 'Departamental'), (2, 'Municipal o Distrital'), (3, 'Club'),(4, 'Escuela'),(5, 'Instituto'))
	tipo 						= models.SmallIntegerField(choices=opt_tipo)
	estado 						= models.BooleanField(default=True)
	opt_caracter_economico 		= ((1,'Privada'),(2,'Pública'),(3,'Mixta'))
	caracter_economico 			= models.SmallIntegerField(choices=opt_caracter_economico)
	ubicacion 					= models.ForeignKey(Ubicacion, null=True)
	telefono					= models.BigIntegerField()
	correo						= models.EmailField(default='informacion@coldeportes.gov.co')
	direccion   				= models.CharField(max_length=50, default='')
	cc_representante_legal		= models.CharField(max_length=20)
	nombre_representante_legal	= models.CharField(max_length=30)
	usuario 					= models.OneToOneField(User, null=True)

	def __str__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		if len(kwargs) == 0:
			codigo = self.nombre.lower()
			self.codigo = codigo
			self.estado = True

			return super(Entidad, self).save(*args, **kwargs)
		else:
			return super(Entidad, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
		return ("detalles_entidad", [self.codigo])

	def get_caracter(self):
		if self.caracter_economico == 1:
			return "Privada"
		elif self.caracter_economico == 2:
			return "Pública"
		else:
			return "Mixta"

	def get_tipo(self):
		if self.tipo == 0:
			return "Rector"
		elif self.tipo == 1:
			return "Departamental"
		elif self.tipo == 2:
			return "Municipal o Distrital"
		elif self.tipo == 3:
			return "Club"
		elif self.tipo == 4:
			return "Escuela"
		else:
			return "Instituto"

class DedicacionEntidad(models.Model):
	id = models.AutoField(primary_key=True)
	entidad = models.ForeignKey(Entidad)
	dedicacion = models.ForeignKey(Dedicacion)

class Escenarios(models.Model):
	codigo 					= models.CharField(max_length=30, primary_key=True)
	nombre 					= models.CharField(max_length=30)
	estado					= models.BooleanField(default=True)
	departamento_ubicacion 	= models.CharField(max_length=30)	
	municipio_ubicacion 	= models.CharField(max_length=30)
	direccion_ubicacion		= models.CharField(max_length=30)
	entidad 				= models.ForeignKey(Entidad)

	def __str__(self):
		return self.nombre

class Deportistas(models.Model):
	nombre 					= models.CharField(max_length=30)
	doc_identidad 			= models.BigIntegerField(primary_key=True)
	fecha_nacim				= models.DateField()
	lugar_nacim				= models.CharField(max_length=20)
	deporte					= models.CharField(max_length=20)
	estado 					= models.BooleanField(default=True)
	categoria				= models.CharField(max_length=10)
	ranking_nacional		= models.CharField(max_length=10)
	ranking_internacional	= models.CharField(max_length=10)
	asociado_a				= models.CharField(max_length=10)
	opt_tipo_asociado		= ((0, 'jugador con pase'), (1, 'jugador asociado con mensualidad'),(2,'jugador asociado con anualidad'))
	tipo_asociado 			= models.SmallIntegerField(choices=opt_tipo_asociado)
	reconocimiento			= models.CharField(max_length=60)

	def __str__(self):
		return self.nombre

	@models.permalink
	def get_absolute_url(self):
		return ("detalles_deportistas", [self.doc_identidad])