from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

"""class LoginForm(ModelForm):

	class Meta:

		model = User
		fields = ['username, password']
		widgets = {
			'username': forms.TextInput(attrs = {
					'class': 'form-control',
					'type': 'text',
					'placeholder': 'usuario'
				}),
			'password': forms.PasswordInput(attrs = {
					'class': 'form-control',
					'type': 'password',
					'placeholder': 'contraseña'
				})
		}"""