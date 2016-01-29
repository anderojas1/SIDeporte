from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User


class MyPrint:

    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter        
        self.width, self.height = self.pagesize

    def print_users(self):

    	buffer = self.buffer
    	doc = SimpleDocTemplate(buffer,
			rightMargin=72,
			leftMargin=72,
			topMargin=72,
			bottomMargin=72,
			pagesize=self.pagesize)

    	elements = []
    	data = []

    	styles = getSampleStyleSheet()
    	styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

    	users = User.objects.all()
    	elements.append(Paragraph('My User Names', styles['Heading1']))
    	for user in users:
    		data.append([user.username, user.password])

    	table = Table(data)
    	table.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
    	elements.append(table)

    	doc.build(elements)
    	pdf = buffer.getvalue()
    	buffer.close()
    	return pdf

class MenuReportesGraficos(TemplateView):
	template_name = 'reportes/menu_reportes_graficos.html'

class ReportesGraficosBarras(TemplateView):
	template_name = 'reportes/reporte_barras.html'

class MenuReportesTablas(TemplateView):
	template_name = 'reportes/menu_reportes_tablas.html'

class ReportesTablas(TemplateView):
	template_name = 'reportes/reporte_tablas.html'
