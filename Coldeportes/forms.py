from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetimewidget.widgets import DateTimeWidget, DateWidget

from .models import Entidad, Ubicacion, Deportistas, DedicacionEntidad, Dedicacion, Deportistas, Escenarios

class FormRegistroEntidad (ModelForm):

	class Meta:
		model = Entidad
		fields = ['codigo', 'nombre', 'tipo', 'estado', 'caracter_economico', 'telefono', 'correo', 'cc_representante_legal', 
		'nombre_representante_legal', 'direccion']
		opt_caracter_economico 	= ((1,'Privada'),(2,'Pública'),(3,'Mixta'))
		opt_tipo = ((0, 'Rector'), (1, 'Departamental'), (2, 'Municipal o Distrital'), (3, 'Club'),(4, 'Escuela'),(5, 'Instituto'))

		widgets = {
			'codigo': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre',
				'type': 'text'
				}),
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
				}),
			'direccion': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Dirección',
				'type': 'text'
				})
		}

class FormRegistroUbicacion (forms.Form):

	departamentos = [('', 'Seleccione un departamento...',)] + 	[(dep.departamento, dep.departamento) for dep in Ubicacion.objects.all().distinct('departamento')] 
	municipios = [('', 'Seleccione un departamento primero...')]
	type = forms.ChoiceField(choices=departamentos, widget=forms.Select(attrs={'onchange': 'get_municipios();', 'class': 'form-control'}))
	municipio = forms.ChoiceField(required=False,choices=municipios, widget=forms.Select(attrs={
		'class': 'form-control',
		'id': 'id_municipio',
		'name': 'municipio'}))

	def clean(self):
		cleaned_data = super(FormRegistroUbicacion, self).clean()
		if cleaned_data['type'] == 'Seleccione un departamento...':
			raise forms.ValidationError("Por favor seleccione un departamento")
		else:
			return cleaned_data

		
class FormRegistroDedicacionEntidad(forms.Form):

	dedicaciones = [(ded.dedicacion, ded.dedicacion) for ded in Dedicacion.objects.all()]
	escoger_dedicaciones = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}), choices=dedicaciones)

class FormRegistroDeportista(ModelForm):

	class Meta:

		model = Deportistas

		opt_tipo_documento = ((0, 'Cédula de ciudadanía'), 
						(1, 'Registro civil'),
						(2,'Tarjeta de identidad'),
						(3, 'Cédula de extranjería'))

		opt_tipo_asociado		= ((0, 'jugador con pase'), (1, 'jugador asociado con mensualidad'),
			(2,'jugador asociado con anualidad'))

		fields = ['nombre', 'tipo_documento', 'doc_identidad', 'fecha_nacim', 'deporte', 'categoria','tipo_asociado']

		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre completo',
				'type': 'text'
				}),
			'tipo_documento': forms.Select(choices=opt_tipo_asociado, attrs={
				'class': 'form-control'
				}),
			'doc_identidad': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Cédula de Ciudadanía',
				}),
			'fecha_nacim': DateWidget(attrs={
				'class': 'form-control',
				'placeholder': 'Seleccione el calendario de la derecha'
				}, bootstrap_version=3, options={
					'format': 'yyyy-mm-dd',
					'picktime': 'false'
				}),
			'deporte': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre completo',
				'type': 'text'
				}),
			'categoria': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre completo',
				'type': 'text'
				}),
			'tipo_asociado': forms.Select(choices=opt_tipo_asociado, attrs={
				'class': 'form-control'
				})

		}

class FormRegistrarEscenario(ModelForm):

	class Meta:

		model = Escenarios
		fields = ['nombre', 'direccion', 'actividad', 'capacidad_publico', 'capacidad_deportistas', 'escala', 'descripcion']

		opt_escala = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))

		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre completo',
				'type': 'text'
				}),
			'direccion': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Dirección',
				'type': 'text'
				}),
			'actividad': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Actividad o deporte practicado',
				'type': 'text'
				}),
			'capacidad_publico': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Capacidad de espectadores'
				}),
			'capacidad_deportistas': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Capacidad de entrenamiento de deportistas'
				}),
			'escala': forms.Select(choices=opt_escala, attrs={
				'class': 'form-control',
				}),
			'descripcion': forms.Textarea(attrs={
				'class': 'form-control',
				'rows': '4',
				'placeholder': 'Ingrese una breve descripción',
				'type': 'text'
				}),
		}