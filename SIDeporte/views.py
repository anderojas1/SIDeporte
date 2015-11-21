from django.shortcuts import render
from django.views.generic import TemplateView

class Index(TemplateView):
	print('ejecuta')
	template_name = 'startbootstrap/pages/index.html'