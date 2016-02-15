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

	print(Ubicacion.objects.all())

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

	dedicaciones = [(ded.id, ded.dedicacion) for ded in Dedicacion.objects.all()]
	print(dedicaciones)
	escoger_dedicaciones = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}), choices=dedicaciones)

class FormRegistroDeportista(ModelForm):

	class Meta:

		model = Deportistas

		opt_deporte = ((0, 'Atletismo'),
						(1, 'Baloncesto'),
						(2, 'Balonmano'),
						(3, 'Béisbol'),
						(4, 'Bicicros'),
						(5, 'Boxeo'),
						(6, 'Equitación'),
						(7, 'Esgrima'),
						(6, 'Fútbol'),
						(7, 'Futsal'),
						(8, 'Gimnasia'),
						(9, 'Golf'),
						(10, 'Halterofilia'),
						(11, 'Hockey'),
						(12, 'Judo'),
						(13, 'Karate'),
						(14, 'Lucha'),
						(15, 'Motociclismo'),
						(16, 'Natación'),
						(17, 'Orientación'),
						(18, 'Patinaje'),
						(19, 'Rugby'),
						(20, 'Sóftbol'),
						(21, 'Skateboard'),
						(21, 'Squash'),
						(22, 'Taekwondo'),
						(23, 'Tenis'),
						(24, 'Tenis de mesa'),
						(25, 'Triatlón'),
						(26, 'Vela'),
						(27, 'Voleibol'),
						(28, 'Volei playa'),
						(29, 'Waterpolo'),
						)

		fields = ['nombre', 'genero','tipo_documento', 'doc_identidad', 'fecha_nacim','lugar_nacimiento', 'deporte_practicado', 'categoria','ranking_nacional','ranking_internacional','tipo_asociado']

		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Nombre completo',
				'type': 'text'
				}),
			'genero': forms.Select(attrs={
				'class': 'form-control'
				}),
			'tipo_documento': forms.Select(attrs={
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
			'lugar_nacimiento':forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Lugar de nacimiento'
				}),
			'deporte_practicado': forms.Select(choices=opt_deporte, attrs={
				'class': 'form-control',
				}),
			'tipo_asociado': forms.Select(attrs={
				'class': 'form-control'
				}),
			'categoria': forms.Select(attrs={
				'class': 'form-control'
				}),
			'ranking_nacional': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Ranking nacional',
				}),
			'ranking_internacional': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Ranking internacional',
				})
		}

class FormRegistrarEscenario(ModelForm):

	class Meta:

		model = Escenarios
		fields = ['nombre', 'direccion', 'capacidad_publico', 'capacidad_deportistas', 'escala', 'descripcion']

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

class FormActividadDedicacion(forms.Form):

	dedicaciones = [('', 'Seleccione una dedicación...',)] + [(dep.id, dep.dedicacion) for dep in Dedicacion.objects.all()]
	actividades = [('', 'Seleccione una dedicación primero')]

	dedicacion = forms.ChoiceField(choices=dedicaciones, widget=forms.Select(attrs={'onchange': 'get_actividades();', 'class': 'form-control'}))
	actividad = forms.ChoiceField(required=False,choices=actividades, widget=forms.Select(attrs={
	'class': 'form-control',
	'id': 'actividad_id',
	'name': 'actividad'}))