from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Entidad, Ubicacion, Deportistas, DedicacionEntidad, Dedicacion
from django.forms.forms import BaseForm

class AsDiv(BaseForm):

	def as_div(self):
	   	return self._html_output(
	        normal_row = u'<div%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</div>',
	        error_row = u'<div>%s</div>',
	        row_ender = '</div>',
	        help_text_html = u' <span class="helptext">%s</span>',
	        errors_on_separate_row = False)


class FormRegistroEntidad (ModelForm):

	class Meta:
		model = Entidad
		fields = ['nombre', 'tipo', 'estado', 'caracter_economico', 'telefono', 'correo', 'cc_representante_legal', 
		'nombre_representante_legal', 'direccion']
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

		
class FormRegistroDedicacionEntidad(forms.Form, AsDiv):

	dedicaciones = [(ded.dedicacion, ded.dedicacion) for ded in Dedicacion.objects.all()]
	escoger_dedicaciones = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}), choices=dedicaciones)