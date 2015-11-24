from django.forms import ModelForm
from django import forms
from .models import Entidad


class FormRegistroEntidad (ModelForm):

	class Meta:
		model = Noticias
		fields = ['nombre', 'tipo', 'estado', 'caracter_economico', 'dedicacion', 'departamento', 'municipio', 'direccion',
				  'telefono', 'cc_representante_legal', 'nombre_representante_legal' ]

		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre',
				'type': 'text'
				}),
			'departamento': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Departamento',
				'type': 'text'
				}),
			'municipio': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Municipio',
				'type': 'text'
				}),
			'direccion': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Direccion ',
				'type': 'text'
				}),
			'cc_representante_legal': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Cedula Ciudadania',
				'type': 'text'
				}),
			'nombre_representante_legal': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre Completo',
				'type': 'text'
				}),
		}
