# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deportistas',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('doc_identidad', models.BigIntegerField(serialize=False, primary_key=True)),
                ('fecha_nacim', models.DateField()),
                ('lugar_nacim', models.CharField(max_length=20)),
                ('deporte', models.CharField(max_length=20)),
                ('categoria', models.CharField(max_length=10)),
                ('ranking_nacional', models.CharField(max_length=10)),
                ('asociado_a', models.CharField(max_length=10)),
                ('tipo_asociado', models.SmallIntegerField(choices=[(0, 'jugador con pase'), (1, 'jugador asociado')])),
                ('reconocimiento', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('codigo', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('tipo', models.SmallIntegerField(choices=[(0, 'rector'), (1, 'Departamento'), (2, 'municipal o distrital'), (3, 'club'), (4, 'escuela'), (5, 'instituto')])),
                ('estado', models.BooleanField(default=True)),
                ('dedicacion', models.SmallIntegerField(choices=[(1, 'deporte'), (2, 'recreacion'), (3, 'aprovechamiento tiempo libre'), (4, 'educacion extraescolar'), (5, 'educacion fisica')])),
                ('telefono', models.BigIntegerField()),
                ('cc_representante_legal', models.BigIntegerField()),
                ('nombre_representante_legal', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Escenarios',
            fields=[
                ('codigo', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('estado', models.BooleanField(default=True)),
                ('departamento_ubicacion', models.CharField(max_length=30)),
                ('municipio_ubicacion', models.CharField(max_length=30)),
                ('direccion_ubicacion', models.CharField(max_length=30)),
                ('entidad', models.ForeignKey(to='Coldeportes.Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('codigo', models.AutoField(serialize=False, primary_key=True)),
                ('departamento', models.CharField(max_length=30)),
                ('municipio', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='entidad',
            name='ubicacion',
            field=models.ForeignKey(to='Coldeportes.Ubicacion'),
        ),
    ]
