# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-08 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prendas', '0020_auto_20181207_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_predido',
            name='observacionesProduccion',
            field=models.TextField(blank=True, help_text='Observaciones para produccion', null=True, verbose_name='Observaciones para produccion'),
        ),
    ]
