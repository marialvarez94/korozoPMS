from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(departamento)
class departamentoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

    def save_model(self,request,obj,form,change):
        obj.nombre = obj.nombre.upper()
        obj.save()
@admin.register(municipio)
class municipioAdmin(admin.ModelAdmin):
    list_display = ('nombre','get_departamento')
    search_fields = ('nombre',)
    list_filter = ('departamento_fk__nombre',)

    def save_model(self,request,obj,form,change):
        obj.nombre = obj.nombre.upper()
        obj.save()

    def get_departamento(self, obj):
        return obj.departamento_fk.nombre
    get_departamento.admin_order_field  = 'departamento_fk'
    get_departamento.short_description = 'Departamento'

