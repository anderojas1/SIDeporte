from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Entidad(models.Model):
	nombre 	= models.CharField(max_length=30, primary_key=True)
	tipo	= ((0, 'rector'), (1, 'Departamento'), (2, 'municipal o distrital'), (3, 'Rural de Difícil Acceso'))
	estado 	= models.BooleanField(default=True)

