from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Entidad, Ubicacion, Deportistas, DedicacionEntidad


class FormRegistroEntidad (ModelForm):

	class Meta:
		model = Entidad
		fields = ['nombre', 'tipo', 'estado', 'caracter_economico', 'telefono', 'correo', 'cc_representante_legal', 
		'nombre_representante_legal' ]
		opt_caracter_economico 	= ((1,'Privada'),(2,'Pública'),(3,'Mixta'))
		opt_tipo = ((0, 'Rector'), (1, 'Departamental'), (2, 'Municipal o Distrital'), (3, 'Club'),(4, 'Escuela'),(5, 'Instituto'))

		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre',
				'type': 'text'
				}),
			'cc_representante_legal': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Cedula Ciudadania',
				'type': 'text'
				}),
			'telefono': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Teléfono',
				'type': 'text'
				}),
			'nombre_representante_legal': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre Completo',
				'type': 'text'
				}),
			'caracter_economico': forms.Select(choices=opt_caracter_economico, attrs={
				'class': 'form-control',
				}),
			'tipo': forms.Select(choices=opt_tipo, attrs={
				'class': 'form-control',
				})
		}

class FormRegistroUbicacion (ModelForm):

	class Meta:
		model = Ubicacion
		fields = ['departamento', 'municipio', 'direccion' ]

		widgets = {
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
		}

		
class FormRegistroDedicacionEntidad(ModelForm):

	class Meta:
		model = DedicacionEntidad
		fields = ['dedicacion']