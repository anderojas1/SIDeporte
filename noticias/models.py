from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Noticias (models.Model):
	codigo 		= models.CharField(max_length=20, primary_key=True)
	titulo 		= models.CharField(max_length=100)
	fecha 		= models.DateField(editable=False)
	imagen 		= models.ImageField(upload_to='imagenes', blank=True)
	contenido 	= models.CharField(max_length=10000)
	estado 		= models.BooleanField(default=True)
	def __str__(self):
		return self.titulo


	def save(self, *args, **kwargs):
		if len(kwargs) == 0:
			fecha = timezone.now().date()
			try:
				consecutivo = str(len(Noticias.objects.filter(fecha=fecha)))
				codigo = str(fecha) + consecutivo
				codigo = codigo.replace('-', '')
			except ObjectDoesNotExist:
				codigo = str(fecha) + "0"
				codigo = codigo.replace('-', '')
			print(codigo)
			self.fecha = fecha
			self.codigo = codigo

			return super(Noticias, self).save(*args, **kwargs)
		else:
			return super(Noticias, self).save(*args, **kwargs)


	@models.permalink
	def get_absolute_url(self):
		return ("detalles_noticia", [self.codigo])

	class Meta:
		verbose_name_plural = "Noticias"
		ordering = ['fecha']