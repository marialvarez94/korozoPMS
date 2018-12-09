# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from suit.sortables import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from easy_thumbnails.files import get_thumbnailer
from usuarios.models import administradores
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.forms import ModelForm, Select, TextInput, NumberInput
from suit_redactor.widgets import RedactorWidget
from suit.widgets import AutosizedTextarea,EnclosedInput
from decimal import *
from django.contrib import messages
from django.shortcuts import redirect



# Register your models here.
#CONFIGURACION DE LOS TEXTFIELD
class Detalle_pedidoForm(ModelForm):
    class Meta:
        widgets = {
            'observaciones': AutosizedTextarea,
            'observaciones_pedido': AutosizedTextarea,
            'observacionesProduccion': AutosizedTextarea,

            # You can also specify html attributes
            'observaciones': AutosizedTextarea(attrs={'rows': 2, 'class': 'input-xlarge'}),
            'observaciones_pedido': AutosizedTextarea(attrs={'rows': 2, 'class': 'input-xlarge'}),
            'observacionesProduccion': AutosizedTextarea(attrs={'rows': 2, 'class': 'input-xlarge'}),

            #'price': EnclosedInput(prepend='$', append='.00'),
        }

# REDACTOR CON OPCIONES MAS SIMPLE
class RedactorMenorForm(ModelForm):
    class Meta:
        widgets = {
            'observaciones_pedido': RedactorWidget(editor_options={'lang': 'es'}),
            'observaciones': RedactorWidget(editor_options={'lang': 'es'}),
            'observacionesProduccion': AutosizedTextarea(attrs={'rows': 2, 'class': 'input-xlarge'}),
            
        }

class RedactorMateriaPrimaForm(ModelForm):
    class Meta:
        widgets = {
            #'composicion': RedactorWidget(editor_options={'lang': 'es'}),
            #'observaciones': RedactorWidget(editor_options={'lang': 'es'})
            'composicion': AutosizedTextarea,

            # You can also specify html attributes
            'composicion': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            
        }

class detalle_prenda_Inline(SortableStackedInline):
    form = Detalle_pedidoForm
    model = Detalle_predido
    min_num = 1
    extra = 0
    raw_id_fields = ('color',)
    verbose_name_plural = 'Pedidos'
    fields = ['codigo_pedido', 'pedido', 'prenda','materia_prima', 'color','promedioPrenda', 'logo', 'ver_foto_admin', ('tipo_logo', 'ubicacion_logo'),'diseno', 'ver_diseno_admin', ('reflectivo', 'ubicacion_reflectivo'), 'observaciones_pedido', 'estado',('fecha_en_corte_inicio','fecha_en_corte_fin'),('fecha_en_confeccion_incio','fecha_en_confeccion_fin'),('fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin'), 'observacionesProduccion','observaciones', 'order']
    suit_classes = 'suit-tab suit-tab-general'
    suit_form_inlines_hide_original = True

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'COMERCIANTE':
                if obj: #Si estoy dentro de la vista del modelo(para editar)
                    if obj.estado == "pendiente":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones','promedioPrenda','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'codigo_pedido', 'materia_prima', 'prenda', 'color', 'logo', 'diseno', 'tipo_logo', 'ubicacion_logo', 'reflectivo', 'ubicacion_reflectivo','observaciones_pedido', 'observacionesProduccion']
                    elif obj.estado == "rechazado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'codigo_pedido','observacionesProduccion']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones','promedioPrenda','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'codigo_pedido', 'materia_prima', 'prenda', 'color', 'logo', 'diseno', 'tipo_logo', 'ubicacion_logo', 'reflectivo', 'ubicacion_reflectivo','observaciones_pedido', 'observacionesProduccion']                    
                else:#Estoy en el crear
                    readonly_fields = ['ver_diseno_admin','codigo_pedido','ver_foto_admin','observaciones','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin','observacionesProduccion']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'EMPRESA':
                if obj:
                    if obj.estado == "pendiente" or obj.estado == "rechazado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones','promedioPrenda','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'codigo_pedido', 'materia_prima', 'prenda', 'color','observacionesProduccion']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones','promedioPrenda','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'codigo_pedido', 'materia_prima', 'prenda', 'color', 'logo', 'diseno', 'tipo_logo', 'ubicacion_logo', 'reflectivo', 'ubicacion_reflectivo','observaciones_pedido','observacionesProduccion']                    
                else:
                    readonly_fields = ['ver_diseno_admin','codigo_pedido','ver_foto_admin','observaciones','estado','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin','observacionesProduccion']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'AUDITOR':
                if obj:
                    if obj.estado == "pendiente" or obj.estado == "rechazado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','diseno', 'codigo_pedido','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin', 'pedido', 'materia_prima', 'prenda', 'color', 'logo', 'tipo_logo', 'ubicacion_logo','reflectivo','ubicacion_reflectivo','observaciones_pedido']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['ver_diseno_admin','ver_foto_admin','observaciones', 'codigo_pedido', 'materia_prima', 'prenda', 'color', 'logo', 'diseno', 'tipo_logo', 'ubicacion_logo', 'reflectivo', 'ubicacion_reflectivo','observaciones_pedido','observacionesProduccion']                    
                else:
                    readonly_fields = ['ver_diseno_admin','ver_foto_admin','codigo_pedido','promedioPrenda', 'pedido', 'materia_prima', 'prenda', 'color', 'logo', 'tipo_logo', 'ubicacion_logo','reflectivo','ubicacion_reflectivo']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser) :
                readonly_fields = ['ver_diseno_admin','ver_foto_admin']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = ['ver_diseno_admin','ver_foto_admin','codigo_pedido']
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields



class configuracion_talla_detpedidoInline(SortableTabularInline):
    model = configuracion_talla_detpedido
    min_num = 0
    extra = 0
    verbose_name_plural = 'Tallas'
    suit_classes = 'suit-tab suit-tab-talla'
    suit_form_inlines_hide_original = True

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'COMERCIANTE':
                if obj:
                    if obj.estado == 'pendiente' or obj.estado == 'rechazado':
                        readonly_fields = ['taller_fk']
                    elif obj.estado == 'aceptado':
                        readonly_fields = ['detalle_pedido_fk','talla_fk','cantidad','taller_fk']
                else:
                    readonly_fields = ['taller_fk']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'EMPRESA':
                if obj:
                    if obj.estado == 'pendiente' or obj.estado == 'rechazado':
                        readonly_fields = ['taller_fk']
                    elif obj.estado == 'aceptado':
                        readonly_fields = ['detalle_pedido_fk','talla_fk','cantidad','taller_fk']
                else:
                    readonly_fields = ['taller_fk']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'AUDITOR':
                if obj:
                    if obj.estado == 'pendiente' or obj.estado == 'rechazado':
                        readonly_fields = ['detalle_pedido_fk','talla_fk','cantidad']
                    elif obj.estado == 'aceptado':
                        readonly_fields = ['detalle_pedido_fk','talla_fk','cantidad']
                else:
                    readonly_fields = ['detalle_pedido_fk','talla_fk','cantidad']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser) :
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = []
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields

  
class Ficha_tecnica_confeccionInline(SortableStackedInline):
    model = Ficha_tecnica_detalle_confeccion
    #form = MovieInlineForm
    min_num = 0
    extra = 0
    verbose_name_plural = 'Detalle confeccion'

    fieldsets = [
        (None, {
            #'classes': ('collapse',),
            'fields': [
                'detalle_pedido_fk','dotacion','pes_puntes','bolsillo','sobrehilo',('color_hilo','amarres'),('recubridora', 'color_recubridora'),('dobladillos','tono'),('puntadas', 'bies'),('entre_tela', 'ojales')
            ]
        })
    ]

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'AUDITOR':
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = ['total_prenda', 'total_pedido']
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields
    suit_classes = 'suit-tab suit-tab-confeccion'
    suit_form_inlines_hide_original = True

class Ficha_tecnica_insumoInline(SortableStackedInline):
    model = Ficha_tecnica_detalle_insumo
    #form = MovieInlineForm
    min_num = 0
    extra = 0
    verbose_name_plural = 'Detalle insumo'

    fieldsets = [
        (None, {
            'fields': ['detalle_pedido_fk',
                ('botones', 'zipper'), ('ubicacion', 'remaches'), ('elastico', 'ubicacion_remache'), ('tallin','garra')
            ]
        })
    ]

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'AUDITOR':
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = ['total_prenda', 'total_pedido']
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields
    suit_classes = 'suit-tab suit-tab-insumo'
    suit_form_inlines_hide_original = True

class Ficha_tecnica_costoForm(ModelForm):
    class Meta:
        widgets = {
            # You can also use prepended and appended together
            'costoCorte': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoConfeccion': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costologo': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoFlete': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoMateriaPrima': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoAdicional': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoFleteEntrada': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'costoFleteDespacho': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),

            # Use HTML for append/prepend (See Twitter Bootstrap docs of supported tags)
            #'url': EnclosedInput(prepend='icon-home', append='<input type="button" class="btn"  value="Open link">'),

        }

class Ficha_tecnica_costoInline(SortableStackedInline):
    model = Ficha_tecnica_detalle_costo
    form = Ficha_tecnica_costoForm
    min_num = 0
    extra = 0
    verbose_name_plural = 'Detalle costos'

    fieldsets = [
        (None, {'fields': ['detalle_pedido_fk'
        ]}),

        ('Costos principales', {
            'fields': [
                'costoCorte', 'costoConfeccion', 'costologo'
                #('costoCorte', 'costoConfeccion'), ('costologo', 'costoFlete'), ('costoFleteEntrada', 'costoFleteDespacho'), ('costoMateriaPrima','costoAdicional'), 'descripcioncostoAdicional', ('total_prenda', 'total_pedido')
            ]
        }),

        ('Costos de flete', {
            'fields': [
                'costoFlete', 'costoFleteEntrada', 'costoFleteDespacho'
                #('costoCorte', 'costoConfeccion'), ('costologo', 'costoFlete'), ('costoFleteEntrada', 'costoFleteDespacho'), ('costoMateriaPrima','costoAdicional'), 'descripcioncostoAdicional', ('total_prenda', 'total_pedido')
            ]
        }),

        ('Costos adicionales', {
            'fields': [
                'costoMateriaPrima', 'costoAdicional', 'descripcioncostoAdicional'
                #('costoCorte', 'costoConfeccion'), ('costologo', 'costoFlete'), ('costoFleteEntrada', 'costoFleteDespacho'), ('costoMateriaPrima','costoAdicional'), 'descripcioncostoAdicional', ('total_prenda', 'total_pedido')
            ]
        }),

        ('Costos totales', {
            'fields': [
                'total_prenda', 'total_pedido'
                #('costoCorte', 'costoConfeccion'), ('costologo', 'costoFlete'), ('costoFleteEntrada', 'costoFleteDespacho'), ('costoMateriaPrima','costoAdicional'), 'descripcioncostoAdicional', ('total_prenda', 'total_pedido')
            ]
        })
    ]

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'AUDITOR':
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = ['total_prenda', 'total_pedido']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = ['total_prenda', 'total_pedido']
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields
    suit_classes = 'suit-tab suit-tab-costo'
    suit_form_inlines_hide_original = True

@admin.register(pedido)
class pedidoAdmin(admin.ModelAdmin):
    view_on_site = False
    suit_form_includes = (
		('informacion_maquinas.html', 'top', 'general'),
		#('maquina/informacion_maquinas_formularios.html', 'top', 'formularios'),
	)
    inlines = (detalle_prenda_Inline,configuracion_talla_detpedidoInline,Ficha_tecnica_insumoInline,Ficha_tecnica_costoInline,Ficha_tecnica_confeccionInline,)
    list_display = ('num_pedido', 'get_cliente', 'get_digitador', 'fecha_creacion', 'fecha_llegada', 'fechaEstimada_entrega','estado')
    search_fields = ('num_pedido','digitador__last_name', 'digitador__first_name')
    list_filter = ('cliente_fk__nombre', 'estado')
    suit_list_filter_horizontal = ('cliente_fk__nombre', 'estado')

    def get_cliente(self, obj):
        return obj.cliente_fk.nombre
    get_cliente.admin_order_field  = 'cliente_fk'
    get_cliente.short_description = 'Empresa'

    def get_digitador(self, obj):
        return "%s" %(obj.digitador.get_full_name())
    get_digitador.admin_order_field  = 'digitador'
    get_digitador.short_description = 'Ejecutivo'

    #ESTILO DE COLORES PARA LAS FILAS DE LA TABLA
    def suit_row_attributes(self, obj, request):
        class_map = {
            'aceptado': 'table-success',
            'pendiente': 'table-warning',
            'rechazado': 'table-danger',
        }

        css_class = class_map.get(obj.estado)
        if css_class:
            return {'class': css_class}

    def save_model(self,request,obj,form,change): # Guardo el usuario logueado en la orden de compra
        if(change==False):
            if len(request.user.groups.all()) > 0:
                if request.user.groups.all()[0].name == 'COMERCIANTE':
                    obj.digitador = request.user
                    obj.estado = 'pendiente'
                elif request.user.groups.all()[0].name == 'EMPRESA':
                    #obj.digitador = request.user
                    obj.cliente_fk = request.user.clientes_fk
                    obj.estado = 'pendiente'
                #FALTA PROGRAMAR QUE PASA EN ESTE CASO
                else:
                    pass
            elif request.user.is_superuser:
                obj.digitador = request.user
            #FALTA PROGRAMAR QUE PASA EN ESTE CASO
            else:
                pass
        obj.save()

    # GUARDA AUTOMATICAMENTE UN CAMPO DE UN INLINE
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Ficha_tecnica_detalle_costo):
                if len(request.user.groups.all()) > 0:
                    if request.user.groups.all()[0].name == 'AUDITOR':
                        
                        pedido_obj = Detalle_predido.objects.get(codigo_pedido = instance.detalle_pedido_fk)
                        cantidad_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk = pedido_obj)
                        cantidad = 0
                        for cant in cantidad_obj:
                            cantidad += cant.cantidad

                        if instance.costoAdicional != None and instance.costoAdicional != "":
                            instance.total_prenda = instance.costoCorte + instance.costoConfeccion + instance.costoFlete + instance.costologo + (instance.costoMateriaPrima * pedido_obj.promedioPrenda) + instance.costoFleteEntrada + instance.costoFleteDespacho + instance.costoAdicional
                            instance.total_pedido = instance.total_prenda * Decimal(cantidad)
                                                                                                            
                        else:
                            instance.total_prenda = instance.costoCorte + instance.costoConfeccion + instance.costoFlete + instance.costologo + (instance.costoMateriaPrima * pedido_obj.promedioPrenda) + instance.costoFleteEntrada + instance.costoFleteDespacho
                            instance.total_pedido = instance.total_prenda * Decimal(cantidad)
                    else:
                        pass
                elif (request.user.is_superuser):
                    pass
            if isinstance(instance, Detalle_predido):
                if len(request.user.groups.all()) > 0:
                    if request.user.groups.all()[0].name == 'COMERCIANTE':
                        instance.estado = "programado"
                        instance.codigo_pedido = "%s-%s-%s-%s" %(instance.pedido.num_pedido,instance.prenda.codigoPrenda.upper(),instance.materia_prima.codigoMP.upper(),instance.color.color.upper())            
                    elif request.user.groups.all()[0].name == 'EMPRESA':
                        instance.estado = "programado"
                        instance.codigo_pedido = "%s-%s-%s-%s" %(instance.pedido.num_pedido,instance.prenda.codigoPrenda.upper(),instance.materia_prima.codigoMP.upper(),instance.color.color.upper())
                elif request.user.is_superuser:
                    pass
            if isinstance(instance, configuracion_talla_detpedido):
                if len(request.user.groups.all()) > 0:
                    if request.user.groups.all()[0].name == 'COMERCIANTE':
                        instance.talla_fk = instance.talla_fk.upper()
                    elif request.user.groups.all()[0].name == 'EMPRESA':
                        instance.talla_fk = instance.talla_fk.upper()
                elif request.user.is_superuser:
                    instance.talla_fk = instance.talla_fk.upper()
                #	instance.empresa_anidada  = im_cliente.objects.get(pk=request.user.im_cliente_id.pk)
            formset.save()

    # RESTRINGE QUIEN PUEDE VER CIERTOS DATOS DEPENDIENDO EL ROL 
    def get_queryset(self, request): #resultado de una consulta
        qs = super(pedidoAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            if request.user.groups.all()[0].name == 'AUDITOR':
                return qs
            elif request.user.groups.all()[0].name == 'COMERCIANTE':
                return qs.filter(digitador__pk = request.user.pk)
            elif request.user.groups.all()[0].name == 'EMPRESA':
                return qs.filter(cliente_fk__pk = request.user.clientes_fk.pk)
        else:
            return qs

    # MUESTRA EN UN SELECT FOREIGN_KEY LOS DATOS FILTRADOS(ej:quien digita la orden de compra)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'digitador':
            grupo = Group.objects.get(name='COMERCIANTE')
            kwargs["queryset"] = administradores.objects.filter(groups__in=[grupo])
        else:
            pass
        return super(pedidoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # MUESTRA LOS CAMPOS ELEGIDOS SOLO PARA LECTURA
    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'COMERCIANTE':                
                if obj:
                    if obj.estado == "pendiente" or obj.estado == "rechazado":
                        readonly_fields = ['estado','cliente_fk','num_pedido','fecha_llegada','digitador','modelo_orden', 'tallaje']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['num_pedido', 'cliente_fk','fecha_llegada', 'fechaEstimada_entrega','modelo_orden','tallaje','estado','digitador']                
                else:
                    readonly_fields = ['estado','digitador']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'EMPRESA':
                if obj:
                    if obj.estado == "pendiente" or obj.estado == "rechazado":
                        readonly_fields = ['estado','cliente_fk','num_pedido','fecha_llegada','modelo_orden', 'tallaje','digitador']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['num_pedido', 'cliente_fk','fecha_llegada', 'fechaEstimada_entrega','modelo_orden', 'tallaje','estado','digitador']                
                else:
                    readonly_fields = ['estado','cliente_fk']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'AUDITOR':
                if obj:
                    if obj.estado == "pendiente" or obj.estado == "rechazado":
                        readonly_fields = ['num_pedido', 'cliente_fk','fecha_llegada', 'fechaEstimada_entrega','modelo_orden','tallaje','digitador']
                    elif obj.estado == "aceptado":
                        readonly_fields = ['num_pedido', 'cliente_fk','fecha_llegada', 'fechaEstimada_entrega','modelo_orden', 'tallaje','estado','digitador']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser) :
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = []
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['num_pedido', 'cliente_fk','digitador', 'fecha_llegada', 'fechaEstimada_entrega', 'modelo_orden', 'tallaje','estado']
        })
    ]

    suit_form_tabs = (
        ('general', 'Subir Pedido'),
        ('talla', 'Tallas'),
        ('confeccion', 'Confeccion'),
        ('insumo', 'Insumos'),
        ('costo', 'Costos'),
    )
    

@admin.register(clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'correo', 'telefono1', 'direccion','get_localizacion','get_foto')
    search_fields = ('nombre', 'nit', 'nombre_comercial')
    list_filter = ('nuw_departamento_fk__nombre',)
    suit_list_filter_horizontal = ('nuw_departamento_fk__nombre',)
    readonly_fields = ('get_foto',)

    def get_localizacion(self, obj):
        if obj.nuw_departamento_fk != None and obj.nuw_departamento_fk != "":
            if obj.municipio_fk != None and obj.municipio_fk != "":
                return "%s - %s" %(obj.nuw_departamento_fk.nombre,obj.municipio_fk.nombre)
            else:
                return "%s" %(obj.nuw_departamento_fk.nombre)
        else:
            return format_html('Sin localizacion')
    get_localizacion.admin_order_field  = 'nuw_departamento_fk'
    get_localizacion.short_description = 'Localizacion'

    def get_queryset(self, request):
        qs = super(ClienteAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            if request.user.groups.all()[0].name == 'EMPRESA':
                return qs.filter(nit = request.user.clientes_fk.nit)
            elif request.user.groups.all()[0].name == 'COMERCIANTE':
                return qs
        else:
            return qs

    fieldsets = [

        (None, {
            'fields': [
                'nit',
                'nombre',
                'nombre_comercial',
                'logo',
                'get_foto',
            ]
        }),
        ("Informacion general", {
            'fields': [
                'direccion',
                'telefono1',
                'telefono2',
                'correo',
            ]
        }),
        ('Localizacion', {
            'fields': [
                'nuw_departamento_fk',
                'municipio_fk',
            ]
        }),
        ("Informacion de contacto", {
            'fields': [
                'nombre_contacto',
                'telefono_contacto',
                'email_contacto',
                'celular_contacto',
            ]
        }),

    ]

@admin.register(proveedores)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_proveedor', 'nit_proveedor', 'correo_proveedor', 'telefono1', 'get_localizacion', 'direccion')
    search_fields = ('nombre_proveedor', 'nit_proveedor', 'encargado')
    list_filter = ('nuw_departamento_fk__nombre',)
    suit_list_filter_horizontal = ('nuw_departamento_fk__nombre',)

    def get_localizacion(self, obj):
        if obj.nuw_departamento_fk != None and obj.nuw_departamento_fk != "":
            if obj.municipio_fk != None and obj.municipio_fk != "":
                return "%s - %s" %(obj.nuw_departamento_fk.nombre,obj.municipio_fk.nombre)
            else:
                return "%s" %(obj.nuw_departamento_fk.nombre)
        else:
            return format_html('Sin localizacion')
    get_localizacion.admin_order_field  = 'nuw_departamento_fk'
    get_localizacion.short_description = 'Localizacion'

    fieldsets = [

        (None, {
            'fields': [
                'nit_proveedor',
                'nombre_proveedor',
                'encargado',
                #'logoProveedor',
                #'ver_foto_admin',
            ]
        }),
        ("Informacion general", {
            'fields': [
                'direccion',
                'telefono1',
                'telefono2',
                'correo_proveedor',
            ]
        }),
        ('Localizacion', {
            'fields': [
                'nuw_departamento_fk',
                'municipio_fk',
            ]
        }),
        ("Informacion de contacto", {
            'fields': [
                'contacto_proveedor',
                'telefono_contacto',
                'email_contacto',
                'celular_contacto',
            ]
        }),

    ]

class Factura_compraForm(ModelForm):
    class Meta:
        widgets = {
            # You can also use prepended and appended together
            'cantidad': EnclosedInput(append='m',attrs={'placeholder': 'Cantidad en metros','class':'col-md-4'}),
            'precio': EnclosedInput(prepend='$', append='.00',attrs={'class':'col-md-3'}),
            'descuento': EnclosedInput(prepend='$', append='%',attrs={'class':'col-md-3'}),

            # Use HTML for append/prepend (See Twitter Bootstrap docs of supported tags)
            #'url': EnclosedInput(prepend='icon-home', append='<input type="button" class="btn"  value="Open link">'),

        }

@admin.register(Factura_CompraMP)
class Factura_compraMPAdmin(admin.ModelAdmin):
    form = Factura_compraForm
    list_display = ('numeroFacturaMP', 'get_proveedor', 'fecha_compra', 'facturaMP_fk','facturaMP_Color_fk', 'precio', 'cantidad', 'descuento', 'total', 'observaciones')
    search_fields = ('numeroFacturaMP','proveedor_fk__nombre_proveedor','facturaMP_fk__nombre','facturaMP_Color_fk__color')
    list_filter = ('proveedor_fk__nombre_proveedor','fecha_compra')
    suit_list_filter_horizontal = ('proveedor_fk__nombre_proveedor','fecha_compra')

    def save_model(self,request,obj,form,change):
        desc = 0
        precio = obj.precio
        cant = obj.cantidad
        try:
            desc = obj.descuento
        except:
            pass
        
        if desc > 0:
            subtotal = (precio * cant)
            descuento = subtotal * (desc/100)
            obj.total = subtotal - descuento
        else:
            obj.total = (precio * cant)

        try:
            upd = Inventario_materia_prima.objects.get(materia_prima_fk = obj.facturaMP_fk, color_fk = obj.facturaMP_Color_fk)
            upd.cantidad = upd.cantidad + obj.cantidad
            upd.save()
        except Inventario_materia_prima.DoesNotExist:
            create = Inventario_materia_prima(materia_prima_fk = obj.facturaMP_fk, color_fk = obj.facturaMP_Color_fk, cantidad = obj.cantidad)
            create.save()

        obj.save()

    # MUESTRA LOS CAMPOS ELEGIDOS SOLO PARA LECTURA
    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'LOGISTICO':
                if obj:
                    readonly_fields = ['fecha_compra','numeroFacturaMP','precio','total','facturaMP_fk','facturaMP_Color_fk','proveedor_fk']
                else:
                    readonly_fields = ['total']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = ['total']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = ['total']
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields

    fieldsets = [

        (None, {
            'fields': [
                'numeroFacturaMP',
                'proveedor_fk',
                'fecha_compra',
            ]
        }),
        ('Detalle de Compra', {
            'fields': [
                'facturaMP_fk',
                'facturaMP_Color_fk',
                'precio',
                'cantidad',
                'descuento',
                'total',
            ]
        }),
    ]

    def get_proveedor(self, obj):
        return obj.proveedor_fk.nombre_proveedor
    get_proveedor.admin_order_field  = 'proveedor_fk'
    get_proveedor.short_description = 'Proveedor'

#------------ADMIN CONTROL DE MATERIA PRIMA
# @admin.register(Control_MateriaPrima)
# class Control_MateriaPrimaAdmin(admin.ModelAdmin):
#     list_display = ('get_facturaCompra','cantidad_gastada')
#     search_fields = ('get_facturaCompra',)
#     suit_list_filter_horizontal = ('FacturaCompraMP_fk__numeroFacturaMP')

#     fieldsets = [

#         (None, {
#             'fields': [
#                 'FacturaCompraMP_fk',
#                 'detallePedidoMP_fk',
#                 'cantidad_gastada',
#                 'stock',
                
#             ]
#         }),
#     ]

#     def get_facturaCompra(self, obj):
#         return obj.FacturaCompraMP_fk.numeroFacturaMP
#     get_facturaCompra.admin_order_field  = 'FacturaCompraMP_fk'
#     get_facturaCompra.short_description = 'Numero de Factura'

#---------------ADMIN Control de prendas---------
@admin.register(Control_Prendas)
class Control_PrendasAdmin(admin.ModelAdmin):
    list_display = ('controlMP_cliente_fk','controlMP_ordenC_fk','controlMP_Detallepedido_fk','talla','cantidad','cantidad_pendiente')
    search_fields = ('controlMP_cliente_fk__nombre',)
    list_filter = ('controlMP_cliente_fk',)
    suit_list_filter_horizontal = ('controlMP_cliente_fk',)

    def save_model(self,request,obj,form,change):
        #conf_talla_obj = configuracion_talla_detpedido.objects.get(pk = obj.pk)
        obj.cantidad_pendiente = obj.talla.cantidad
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'EMPRESA':
                if obj:
                    readonly_fields = ['cantidad_pendiente','controlMP_cliente_fk','controlMP_ordenC_fk','cantidad','talla','controlMP_Detallepedido_fk']
                else:
                    readonly_fields = ['cantidad_pendiente']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'LOGISTICO':
                if obj:
                    readonly_fields = ['cantidad_pendiente','controlMP_cliente_fk','controlMP_ordenC_fk','talla','controlMP_Detallepedido_fk']
                else:
                    readonly_fields = ['cantidad_pendiente']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = []
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields

    def get_queryset(self, request):
        qs = super(Control_PrendasAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            if request.user.groups.all()[0].name == 'EMPRESA':
                return qs.filter(controlMP_cliente_fk__nit = request.user.clientes_fk.nit)
            else:
                return qs
            # elif request.user.groups.all()[0].name == 'COMERCIANTE':
            #     return qs
        else:
            return qs

    fieldsets = [

        (None, {
            'fields': [
                'controlMP_cliente_fk',
                'controlMP_ordenC_fk',
                'controlMP_Detallepedido_fk',
                'talla',
                'cantidad',
                'cantidad_pendiente',
                
            ]
        }),
    ]

@admin.register(Inventario_Prendas)
class Inventario_PrendasAdmin(admin.ModelAdmin):
    list_display = ('get_inventarioPrenda','get_inventarioMP','get_inventarioColor','talla','cantidad')
    search_fields = ('inventarioPrenda_fk__tipo_prenda','inventarioMP_fk__nombre','inventarioColor_fk__color')
    list_filter = ('inventarioMP_fk','inventarioPrenda_fk')
    suit_list_filter_horizontal = ('inventarioMP_fk','inventarioPrenda_fk')

    def save_model(self,request,obj,form,change):
        try:
            if change == True:
                upd = Inventario_Prendas.objects.get(inventarioPrenda_fk = obj.inventarioPrenda_fk, inventarioMP_fk = obj.inventarioMP_fk, inventarioColor_fk = obj.inventarioColor_fk, talla = obj.talla.upper())
                upd.cantidad = obj.cantidad
                upd.save()
            elif change == False:
                upd = Inventario_Prendas.objects.get(inventarioPrenda_fk = obj.inventarioPrenda_fk, inventarioMP_fk = obj.inventarioMP_fk, inventarioColor_fk = obj.inventarioColor_fk, talla = obj.talla.upper())
                #messages.error(request, 'El inventario de prenda ya se encuentra guardado!')
                mensaje = "El inventario de prenda ya se encuentra guardado!"
                messages.set_level(request, messages.ERROR)
                messages.error(request,mensaje)
        except Inventario_Prendas.DoesNotExist:
            create = Inventario_Prendas(inventarioPrenda_fk = obj.inventarioPrenda_fk, inventarioMP_fk = obj.inventarioMP_fk, inventarioColor_fk = obj.inventarioColor_fk, talla = obj.talla.upper(), cantidad = obj.cantidad)
            create.save()

    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'AUDITOR':
                if obj:
                    readonly_fields = ['inventarioPrenda_fk','inventarioMP_fk','inventarioColor_fk','talla']
                else:
                    readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'LOGISTICO':
                if obj:
                    readonly_fields = ['inventarioPrenda_fk','inventarioMP_fk','inventarioColor_fk','talla']
                else:
                    readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = []
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields

    fieldsets = [

        (None, {
            'fields': [
                'inventarioPrenda_fk',
                'inventarioMP_fk',
                'inventarioColor_fk',
                'talla',
                'cantidad',
                
            ]
        }),
    ]

    def get_inventarioPrenda(self, obj):
        return obj.inventarioPrenda_fk.tipo_prenda
    get_inventarioPrenda.admin_order_field  = 'inventarioPrenda_fk'
    get_inventarioPrenda.short_description = 'Prenda'

    def get_inventarioMP(self, obj):
        return obj.inventarioMP_fk.nombre
    get_inventarioMP.admin_order_field  = 'inventarioMP_fk'
    get_inventarioMP.short_description = 'Materia Prima'

    def get_inventarioColor(self, obj):
        return obj.inventarioColor_fk.color
    get_inventarioColor.admin_order_field  = 'inventarioColor_fk'
    get_inventarioColor.short_description = 'Color'

@admin.register(prenda)
class prendaAdmin(admin.ModelAdmin):
    list_display = ('codigoPrenda','tipo_prenda')
    search_fields = ('tipo_prenda',)

    def save_model(self,request,obj,form,change):
        obj.tipo_prenda = obj.tipo_prenda.upper()
        obj.save()

class colorInline(SortableTabularInline):
    model = color
    filter_horizontal = ('proveedor_fk',)
    min_num = 1
    extra = 0
    verbose_name_plural = 'Colores'
    #suit_form_inlines_hide_original = True

    # MUESTRA LOS CAMPOS ELEGIDOS SOLO PARA LECTURA
    def get_readonly_fields(self, request, obj=None):
        if len(request.user.groups.all()) > 0:
            if request.user.groups.all()[0].name == 'COMERCIANTE':
                readonly_fields = ['proveedor_fk']
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif request.user.groups.all()[0].name == 'LOGISTICO':
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
            elif (request.user.is_superuser):
                readonly_fields = []
                if 'is_submitted' in readonly_fields:
                    readonly_fields.remove('is_submitted')
                return readonly_fields
        elif (request.user.is_superuser) :
            readonly_fields = []
            if 'is_submitted' in readonly_fields:
                 readonly_fields.remove('is_submitted')
            return readonly_fields


@admin.register(materia_prima)
class materia_primaAdmin(admin.ModelAdmin):
    form = RedactorMateriaPrimaForm
    #inlines = (colorInline,) Esto es cuando llenan la MP tambien llenen el color
    list_display = ('codigoMP','nombre','composicion')
    search_fields = ('nombre',)

    def save_model(self,request,obj,form,change):
        obj.nombre = obj.nombre.upper()
        obj.save()

@admin.register(Taller)
class tallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'get_localizacion', 'direccion')
    search_fields = ('nombre',)
    list_filter = ('nuw_departamento_fk__nombre',)
    suit_list_filter_horizontal = ('nuw_departamento_fk__nombre',)

    def get_localizacion(self, obj):
        if obj.nuw_departamento_fk != None and obj.nuw_departamento_fk != "":
            if obj.municipio_fk != None and obj.municipio_fk != "":
                return "%s - %s" %(obj.nuw_departamento_fk.nombre,obj.municipio_fk.nombre)
            else:
                return "%s" %(obj.nuw_departamento_fk.nombre)
        else:
            return format_html('Sin localizacion')
    get_localizacion.admin_order_field  = 'nuw_departamento_fk'
    get_localizacion.short_description = 'Localizacion'

    fieldsets = [

        (None, {
            'fields': [
                'nombre',
                #'logoProveedor',
                #'ver_foto_admin',
            ]
        }),
        ("Informacion general", {
            'fields': [
                'direccion',
                'telefono',
                'correo',
            ]
        }),
        ('Localizacion', {
            'fields': [
                'nuw_departamento_fk',
                'municipio_fk',
            ]
        }),
        ("Informacion de contacto", {
            'fields': [
                'nombre_contacto',
                'telefono_contacto',
                'email_contacto',
                'celular_contacto',
            ]
        }),

    ]

@admin.register(Detalle_predido)
class DetallePedidoAdmin(admin.ModelAdmin):
    form = RedactorMenorForm
    list_display = ('codigo_pedido','pedido','get_empresa','get_prenda','get_materia_prima','get_color','get_talla', 'get_cantidad_tela','cant_asig_mp','get_estadoOrden','estado','inventario','impresion','file_link')
    search_fields = ('codigo_pedido','pedido__num_pedido')
    list_filter = ('materia_prima__nombre','prenda__tipo_prenda','pedido__estado','estado')
    suit_list_filter_horizontal = ('materia_prima__nombre','pedido__estado','prenda__tipo_prenda','estado')
    readonly_fields=['ver_diseno_admin','ver_foto_admin','codigo_pedido','pedido','materia_prima','prenda','color','estado','logo','diseno','tipo_logo','ubicacion_logo','reflectivo','ubicacion_reflectivo','observaciones_pedido','fecha_en_corte_inicio','fecha_en_corte_fin','fecha_en_confeccion_incio','fecha_en_confeccion_fin','fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin','observaciones', 'promedioPrenda','observacionesProduccion']
    raw_id_fields = ("color",)

    def impresion(self, obj):
        if obj.estado == 'encorte':
            return format_html('<button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="corte(%s)" title="Generar orden de corte"><img src="/static/imagenes/cut.svg" height="15px" /></button> <br> <button disabled type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="confeccion(%s)" title="Generar orden de confeccion"><img src="/static/imagenes/confe.svg" height="15px" /></button> <br> <button disabled type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="logo(%s)" title="Generar orden de diseno de logo"><img src="/static/imagenes/dise.svg" height="15px"/></button><br>'%(obj.pk,obj.pk,obj.pk))
        elif obj.estado == 'enconfeccion':
            return format_html('<button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="corte(%s)" title="Generar orden de corte"><img src="/static/imagenes/cut.svg" height="15px" /></button> <br> <button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="confeccion(%s)" title="Generar orden de confeccion"><img src="/static/imagenes/confe.svg" height="15px" /></button> <br> <button disabled type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="logo(%s)" title="Generar orden de diseno de logo"><img src="/static/imagenes/dise.svg" height="15px"/></button><br>'%(obj.pk,obj.pk,obj.pk))
        elif obj.estado == 'endisenologo':
            return format_html('<button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="corte(%s)" title="Generar orden de corte"><img src="/static/imagenes/cut.svg" height="15px" /></button> <br> <button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="confeccion(%s)" title="Generar orden de confeccion"><img src="/static/imagenes/confe.svg" height="15px" /></button> <br> <button  type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="logo(%s)" title="Generar orden de diseno de logo"><img src="/static/imagenes/dise.svg" height="15px"/></button><br>'%(obj.pk,obj.pk,obj.pk))
        elif obj.estado == 'despachado':
            return format_html('<button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="corte(%s)" title="Generar orden de corte"><img src="/static/imagenes/cut.svg" height="15px" /></button> <br> <button type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="confeccion(%s)" title="Generar orden de confeccion"><img src="/static/imagenes/confe.svg" height="15px" /></button> <br> <button  type="button" class="btn btn-primary" style="background-color: #FEA43F; border-color: #FEA43F;" onclick="logo(%s)" title="Generar orden de diseno de logo"><img src="/static/imagenes/dise.svg" height="15px"/></button><br>'%(obj.pk,obj.pk,obj.pk)) 
    impresion.short_description = 'Imprimir Ordenes'
    

    def inventario(self, obj):
        prom_tela = 0
        tela = 0
        tallas = []
        try:
            prom_tela = obj.promedioPrenda
        except:
            pass

        #get cantidad de prendas
        detalle_pk = obj.codigo_pedido
        cantidad_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__codigo_pedido = detalle_pk)
        
        for cant in cantidad_obj:
            tela += cant.cantidad
            tallas.append(cant.talla_fk)

        cantidad_comprar = tela * prom_tela
        if cantidad_comprar > 0:
            return format_html('<button type="button" class="btn btn-primary" id="logistico_asig" onclick="inv_mat_prima(%s,%s,%s,%s)">Inventario <br>materia prima</button> <br><br> <button type="button" class="btn btn-primary" id="inv_prendas" onclick="inv_prenda(%s,%s,%s,%s,%s)">Inventario de<br>prendas</button>'%(obj.materia_prima.pk,obj.color.pk,cantidad_comprar,obj.pk,obj.materia_prima.pk,obj.color.pk,obj.prenda.pk,tela,obj.pk))
    inventario.short_description = 'Inventario'

    def get_pedido(self, obj):
        return obj.pedido.num_pedido
    get_pedido.admin_order_field  = 'pedido'
    get_pedido.short_description = 'Orden de Compra'

    def get_empresa(self, obj):
        return obj.pedido.cliente_fk.nombre
    get_empresa.short_description = 'Empresa'




    def get_materia_prima(self, obj):
        return obj.materia_prima.nombre
    get_materia_prima.admin_order_field  = 'materia_prima'
    get_materia_prima.short_description = 'Materia prima' #Como se muestra

    def get_color(self, obj):
        return obj.color.color
    get_color.admin_order_field  = 'color'
    get_color.short_description = 'Color'

    def get_prenda(self, obj):
        return obj.prenda.tipo_prenda
    get_prenda.admin_order_field  = 'prenda'
    get_prenda.short_description = 'Prenda' 

    def get_estadoOrden(self,obj):
        return obj.pedido.estado
    get_estadoOrden.short_description = 'Estado de Orden'





    def get_cantidad_tela(self, obj):
        prom_tela = 0
        tela = 0
        try:
            prom_tela = obj.promedioPrenda
        except:
            pass

        #get cantidad de prendas
        detalle_pk = obj.codigo_pedido
        cantidad_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__codigo_pedido = detalle_pk)
        
        for cant in cantidad_obj:
            tela += cant.cantidad

        cantidad_comprar = tela * prom_tela
        return cantidad_comprar
    get_cantidad_tela.short_description = 'Cantidad de tela requerida (m)'

    def get_talla(self, obj):
        detalle_pk = obj.codigo_pedido
        talla_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__codigo_pedido = detalle_pk)
        tallas = []
        for talla in talla_obj:
            tallas.append(talla.talla_fk)
        return tallas
    get_talla.short_description = 'Tallas'

    
   

    # def get_inventario_materia_prima(self, obj):
    # get_inventario_materia_prima.short_description = 'Inventario materia prima'

    fieldsets = [

        (None, {
            'fields': [
                'codigo_pedido',
                'pedido',
                'materia_prima',
                'color',
                'prenda',
                'promedioPrenda',
            ]
        }),
        ("Diseño y logo", {
            'fields': [
                'diseno',
                'ver_diseno_admin',
                'logo',
                'ver_foto_admin',
                ('tipo_logo','ubicacion_logo'),
                ('reflectivo','ubicacion_reflectivo'),
            ]
        }),
        ('Estados', {
            'fields': [
                'estado',
                ('fecha_en_corte_inicio','fecha_en_corte_fin'),
                ('fecha_en_confeccion_incio','fecha_en_confeccion_fin'),
                ('fecha_en_diseno_logo_inicio','fecha_en_diseno_logo_fin'),
            ]
        }),
        ("Observaciones", {
            'fields': [
                'observaciones_pedido',
                'observacionesProduccion',
                'observaciones',
            ]
        }),

    ]

@admin.register(Inventario_materia_prima)
class inven_materia_primaAdmin(admin.ModelAdmin):
    list_display = ('materia_prima_fk','color_fk','cantidad')
    list_filter = ('materia_prima_fk__nombre',)
    suit_list_filter_horizontal = ('materia_prima_fk__nombre',)
    search_fields = ('materia_prima_fk__nombre','color_fk__color')
    readonly_fields = ('materia_prima_fk','color_fk')


@admin.register(color)
class colorAdmin(admin.ModelAdmin):
    filter_horizontal = ('proveedor_fk',)
    list_display = ('codigoColor','color','materia_prima_fk')
    list_filter = ('materia_prima_fk__nombre','proveedor_fk__nombre_proveedor',)
    

    