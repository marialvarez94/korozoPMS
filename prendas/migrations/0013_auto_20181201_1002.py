# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-01 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prendas', '0012_remove_pedido_tallaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia_prima',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Materia prima'),
        ),
    ]