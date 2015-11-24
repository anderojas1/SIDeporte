from django.contrib import admin
from .models import Ubicacion , Entidad, Escenarios, Deportistas

# Register your models here.

admin.site.register(Ubicacion)
admin.site.register(Entidad)
admin.site.register(Escenarios)
admin.site.register(Deportistas)