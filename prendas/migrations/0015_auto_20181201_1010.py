# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-01 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prendas', '0014_auto_20181201_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='tallaje',
            field=models.FileField(blank=True, null=True, upload_to='uploads/pedidos/tallajes', verbose_name='Tallaje'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='modelo_orden',
            field=models.FileField(blank=True, null=True, upload_to='uploads/pedidos/ordenes', verbose_name='Modelo de orden'),
        ),
    ]