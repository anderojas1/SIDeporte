from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
#from .forms import LoginForm

class Index(TemplateView):
	template_name = 'startbootstrap/pages/index.html'


"""class Login(TemplateView):
	template_name = 'startbootstrap/pages/login.html'
	loginform = LoginForm

	def get_context_data(self, **kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		if 'loginform' not in context:
			context['loginform'] = self.loginform

		return context

	def post(self, request, *args, **kwargs):
		self.loginform = LoginForm(request.POST)
		if self.loginform.is_valid():
			usuario = self.loginform.cleaned_data['username']
			password = self.loginform.cleaned_data['password']

			user = authenticate(username=username, password=password)

			if user is not None and user.is_active:
				login(request, user)
				return render (request, '/')"""