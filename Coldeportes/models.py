from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Create your models here.


class Ubicacion(models.Model):
	codigo 		= models.AutoField(primary_key=True)
	departamento= models.CharField(max_length=30)	
	municipio 	= models.CharField(max_length=30)
	direccion	= models.CharField(max_length=30)

	def __int__(self):
		return self.codigo

class Dedicacion(models.Model):
	id = models.AutoField(primary_key=True)
	opt_dedicacion				= ((1,'deporte'),(2,'recreacion'),(3,'aprovechamiento tiempo libre'),(4,'educacion extraescolar'),(5,'educacion fisica'))
	dedicacion 					= models.SmallIntegerField(choices=opt_dedicacion)

	def __str__(self):
		
		if self.dedicacion == 1:  
			return str('deporte')
			
		if self.dedicacion == 2:
			return str('recreacion')

		if self.dedicacion == 3:
			return str('aprovechamiento tiempo libre')

		if self.dedicacion == 4:
			return str('educacion extraescolar')

		if self.dedicacion == 5:
			return str('educacion fisica')


		

class Entidad(models.Model):
	codigo 						= models.CharField(max_length=30, primary_key=True)
	nombre 						= models.CharField(max_length=30)
	opt_tipo					= ((0, 'rector'), (1, 'Departamento'), (2, 'municipal o distrital'), (3, 'club'),(4, 'escuela'),(5, 'instituto'))
	tipo 						= models.SmallIntegerField(choices=opt_tipo)
	estado 						= models.BooleanField(default=True)
	dedicacion 					= models.ManyToManyField(Dedicacion)
	opt_caracter_economico 		= ((1,'privada'),(2,'publica'),(3,'mixta'))
	caracter_economico 			= models.SmallIntegerField(choices=opt_caracter_economico)
	ubicacion 					= models.ForeignKey(Ubicacion)
	telefono					= models.BigIntegerField()
	correo						= models.EmailField(default='informacion@coldeportes.gov.co')
	cc_representante_legal		= models.BigIntegerField()
	nombre_representante_legal	= models.CharField(max_length=30)
	usuario 					= models.OneToOneField(User, default=1)

	def __str__(self):
		return self.nombre

class Escenarios(models.Model):
	codigo 					= models.CharField(max_length=30, primary_key=True)
	nombre 					= models.CharField(max_length=30)
	estado 					= models.BooleanField(default=True)
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