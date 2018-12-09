# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from prendas.models import clientes
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html


# Create your models here.
class administradores(AbstractUser):
    GENERO_CHOICE=(
        ('femenino','Femenino'),
        ('masculino','Masculino'),
    )
    clientes_fk = models.ForeignKey(clientes, verbose_name='Empresa', blank=True, null=True,help_text="Aqui debe asignar el cliente al cual pertenece este usuario")
    cedula = models.PositiveIntegerField(verbose_name="Cedula ",unique=True, blank=True, null=True)
    genero = models.CharField(choices=GENERO_CHOICE, verbose_name="Genero ", max_length=25, blank=True, null=True)
    direccion = models.CharField(verbose_name="Direccion ", max_length=255, blank=True, null=True)
    telefono = models.PositiveIntegerField(verbose_name="Telefono ", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def cambiar_contrasenia(self):
		return format_html("Las contraseñas sin procesar no se almacenan, por lo que no hay manera de ver la contraseña de este usuario, pero puede cambiar la contraseña usando <a  style=  'color: #fed340 !important;font-weight: bold !important;' href=\"/admin/Usuarios/administradores/"+str(self.pk)+"/password\">este formulario</a>.")
    cambiar_contrasenia.short_description='Cambiar contraseña'

    def Nombre_apellido(self):
        return "%s %s" %(self.first_name, self.last_name)
    Nombre_apellido.short_description="Nombres y Apellidos"

    def __unicode__(self):
        return "%s %s" %(self.first_name, self.last_name)
