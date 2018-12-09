from __future__ import unicode_literals

from django.db import models

# Create your models here.
class departamento(models.Model):
    nombre = models.CharField(verbose_name="Departamento", max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Departamento'
        verbose_name_plural = u'Departamentos'

class municipio(models.Model):
    departamento_fk = models.ForeignKey(departamento, verbose_name='Departamento')
    nombre = models.CharField(verbose_name="Municipio", max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = u'Municipio'
        verbose_name_plural = u'Municipios'