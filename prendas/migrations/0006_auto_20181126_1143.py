# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-26 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prendas', '0005_detalle_predido_modelo_orden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_predido',
            name='modelo_orden',
        ),
        migrations.AddField(
            model_name='pedido',
            name='modelo_orden',
            field=models.FileField(blank=True, null=True, upload_to='uploads/pedidos/ordenes', verbose_name='modelo de orden'),
        ),
    ]
