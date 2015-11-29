from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView


class MenuReportesGraficos(TemplateView):
	template_name = 'reportes/menu_reportes_graficos.html'

class ReportesGraficosBarras(TemplateView):
	template_name = 'reportes/reporte_barras.html'

class MenuReportesTablas(TemplateView):
	template_name = 'reportes/menu_reportes_tablas.html'

class ReportesTablas(TemplateView):
	template_name = 'reportes/reporte_tablas.html'