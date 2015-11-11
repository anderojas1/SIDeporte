# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noticias',
            fields=[
                ('codigo', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('titulo', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('imagen', models.ImageField(upload_to='imagenes')),
                ('contenido', models.CharField(max_length=1000)),
            ],
        ),
    ]
