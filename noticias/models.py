from django.db import models

# Create your models here.

class Noticias (models.Model):
	codigo = models.CharField(max_length=20, primary_key=True)
	titulo = models.CharField(max_length=100)
	fecha = models.DateField()
	imagen = models.ImageField(upload_to='imagenes')
	contenido = models.CharField(max_length=1000)

	def __str__(self):
		return self.titulo

	class Meta:
		verbose_name_plural = 'Noticias'