from django.forms import ModelForm
from django import forms
from .models import Noticias


class FormRegistroNoticias (ModelForm):

	class Meta:
		model = Noticias
		fields = ['titulo', 'contenido', 'imagen']
		widgets = {
			'titulo': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Ingrese un título',
				'type': 'text'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control',
				'rows': '6',
				'placeholder': 'Ingrese el contenido',
				'type': 'text'
				}),
			'imagen': forms.FileInput(attrs={
				'type': 'file'
				})
		}

	def clean(self):
		cleaned_data = super(FormRegistroNoticias, self).clean()
		if cleaned_data['imagen'] == None:
			raise forms.ValidationError("El archivo con imagen es requerida")

class FormEdicionNoticias (ModelForm):

	class Meta:
		model = Noticias
		fields = ['titulo', 'contenido', 'imagen']
		widgets = {
			'titulo': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Ingrese un título',
				'type': 'text'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control',
				'rows': '6',
				'placeholder': 'Ingrese el contenido',
				'type': 'text'
				}),
			'imagen': forms.FileInput(attrs={
				'type': 'file'
				})
		}
