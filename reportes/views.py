from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.views.generic import TemplateView
from io import BytesIO
from django.views.generic.edit import DeleteView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User
from Coldeportes.models import *
from Coldeportes.grupos import InformacionUsuario


class PDFReport:

    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter        
        self.width, self.height = self.pagesize

    def print_elements(self, lista, encabezado):

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

        elements.append(Paragraph(encabezado, styles['Heading1']))

        if "Ranking" in encabezado:
            data.append(['Nombre', 'Fecha nacimiento', 'Lugar nacimiento', 'Posición', 'Entidad'])
            for dep in lista:
                data.append([dep.nombre, dep.fecha_nacim, dep.lugar_nacimiento, dep.ranking_nacional,
                    dep.entidad.codigo])

        elif "Deportistas" in encabezado and "adscritos" in encabezado:
            data.append(['Nombre', 'Fecha de nacimiento', 'Lugar de nacimiento', 'Deporte que practica'])
            for dep in lista:
                data.append([dep.nombre, dep.fecha_nacim, dep.lugar_nacimiento, dep.deporte_practicado])

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

class ReporteRankingNacionalDeporte(TemplateView):
  template_name = 'reportes/ranking-nacional-deporte.html'
  deporte_esc = None

  def get_context_data(self, **kwargs):
    context = super(ReporteRankingNacionalDeporte, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    context['inicio'] = 'inicio'
    context['deportes'] = self.get_deportes()

    return context

  def get_deportes (self):
    dedicacion = Dedicacion.objects.get(dedicacion='Deporte')
    deportes = Actividades.objects.filter(tipo_actividad=dedicacion).order_by("actividad")

    return deportes

  def post(self, request, *args, **kwargs):
    context = super(ReporteRankingNacionalDeporte, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    if 'pdf' not in request.POST:
      deporte_seleccionado = request.POST['deporte']

      if len(deporte_seleccionado) > 0:

        self.deporte_esc = Actividades.objects.get(codigo=deporte_seleccionado)
        deportistas = Deportistas.objects.filter(deporte_practicado=self.deporte_esc).order_by("ranking_nacional")

        if len(deportistas) > 0:
          context['deportistas'] = deportistas
          context['deporte'] = self.deporte_esc

        else:
          context['vacio'] = 'No hay deportistas registrados para el deporte ' + self.deporte_esc.actividad
          context['inicio'] = "inicio"
          context['deportes'] = self.get_deportes()

      else:
        context['invalido'] = 'Debe seleccionar un deporte'
        context['inicio'] = "inicio"
        context['deportes'] = self.get_deportes()

    else:

      self.deporte_esc = Actividades.objects.get(codigo=int(request.POST['pdf']))  
      deportistas = Deportistas.objects.filter(deporte_practicado=self.deporte_esc).order_by("ranking_nacional")

      response = HttpResponse(content_type='application/pdf')
      filename = 'ranking_nacional_' + self.deporte_esc.actividad + '.pdf'
      encabezado = 'Ranking Nacional de ' + self.deporte_esc.actividad
      buffer = BytesIO()
      report = PDFReport(buffer, 'A4')
      pdf = report.print_elements(deportistas, encabezado)
      response.write(pdf)
      return response
    return render(request, self.template_name, context)

class ReporteDeportistasEntidad (TemplateView):
  template_name = 'reportes/deportistas-entidad.html'

  def get_entidades(self):
    entidades = Entidad.objects.all().order_by('nombre')
    return entidades

  def get_context_data(self, **kwargs):
    context = super(ReporteDeportistasEntidad, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    context['get'] = 'get'
    context['entidades'] = self.get_entidades()

    return context

  def post(self, request, *args, **kwargs):
    context = super(ReporteDeportistasEntidad, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    if 'pdf' not in request.POST:
      entidad = request.POST['entidad']
      entidad_esc = Entidad.objects.get(codigo=entidad)

      if len(entidad) > 0:

        deportistas = Deportistas.objects.filter(entidad=entidad)

        if len(deportistas) > 0:
          context['deportistas'] = deportistas
          context['entidad'] = entidad
          context['post'] = 'POST'

        else:
          context['vacio'] = 'No hay deportistas adscritos a ' + entidad_esc.nombre
          context['get'] = 'get'
          context['entidades'] = self.get_entidades()

      else:
        context['invalido'] = 'Debe seleccionar una entidad de la lista'
        context['get'] = 'get'
        context['entidades'] = self.get_entidades()

    else:
      print(request.POST)
      entidad = Entidad.objects.get(codigo=request.POST['pdf'])
      deportistas = Deportistas.objects.filter(entidad=entidad)

      response = HttpResponse(content_type='application/pdf')
      filename = 'deportistas_adscritos_' + entidad.codigo + '.pdf'
      encabezado = 'Deportistas adscritos a ' + entidad.codigo
      buffer = BytesIO()
      report = PDFReport(buffer, 'A4')
      pdf = report.print_elements(deportistas, encabezado)
      response.write(pdf)
      return response

    return render(request, self.template_name, context)

class ReporteDeportistasGenero(TemplateView):
  template_name = 'reportes/deportistas-genero.html'

  def get_context_data(self, **kwargs):
    context = super(ReporteDeportistasGenero, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    deportistas_m = Deportistas.objects.filter(genero=0)
    deportistas_f = Deportistas.objects.filter(genero=1)
    deportistas_o = Deportistas.objects.filter(genero=2)

    context['deportistas_m'] = deportistas_m
    context['deportistas_f'] = deportistas_f
    context['deportistas_o'] = deportistas_o

    return context


class ReporteNumeroDeportistasEntidad(TemplateView):
  template_name = 'reportes/deportistas_entidad_num.html'

  def get_context_data(self, **kwargs):
    context = super(ReporteNumeroDeportistasEntidad, self).get_context_data(**kwargs)

    ver_grupo = InformacionUsuario()
    grupo = ver_grupo.asignarGrupo(self.request.user)
    context[grupo] = grupo

    entidades = Entidad.objects.all()
    depor_entidad = []

    for entidad in entidades:
      numero = len(Deportistas.objects.filter(entidad=entidad))
      if numero > 0:
        entidad_numero = (entidad.codigo, numero)
        depor_entidad.append(entidad_numero)

    context['depor_entidad'] = depor_entidad

    return context