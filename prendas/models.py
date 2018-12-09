# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from localizacion.models import *
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer
from smart_selects.db_fields import ChainedForeignKey
from decimal import Decimal

#from usuarios.models import administradores


# Create your models here.
class clientes(models.Model):
    nit = models.CharField(max_length=50, verbose_name='N.I.T.', unique=True)
    nombre=models.CharField(max_length=255,verbose_name="Razon social")
    nombre_comercial = models.CharField(max_length=255,verbose_name="Nombre comercial", blank=True, null=True)
    correo=models.EmailField(max_length=255,verbose_name="Correo Electronico", blank=True, null=True)
    telefono1=models.CharField(max_length=255,verbose_name="Telefono 1", blank=True, null=True)
    telefono2=models.CharField(max_length=255,verbose_name="Telefono 2", blank=True, null=True)
    direccion=models.CharField(max_length=255,verbose_name="Direccion", blank=True, null=True)

    nombre_contacto = models.CharField(max_length=150, verbose_name='Nombre de contacto', blank=True, null=True)
    telefono_contacto = models.CharField(max_length=50, verbose_name='Telefono de contacto', blank=True, null=True)
    email_contacto = models.EmailField(max_length=255, verbose_name='Correo Electronico del contacto', blank=True, null=True)
    celular_contacto = models.CharField(max_length=100, verbose_name='Celular del contacto', blank=True, null=True)

    nuw_departamento_fk = models.ForeignKey("localizacion.departamento", verbose_name='Departamento', blank=True, null=True)
    municipio_fk = ChainedForeignKey(
        'localizacion.municipio',
        chained_field="nuw_departamento_fk",
        chained_model_field="departamento_fk",
        show_all=False,
        auto_choose=True, 
        verbose_name="Municipio",
        blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    logo=models.ImageField(upload_to='uploads/fotos/clientes/',verbose_name="Logo",blank=True, null=True)

    def get_foto(self):
        if self.logo != None and self.logo != "":
            foto = get_thumbnailer(self.logo)['avatar'].url
            return format_html('<img src="%s">'%(foto))
        else:
            return format_html("<b>Sin Logo</b>")
    get_foto.short_description = 'Logo'

    # def get_foto(self):
    #     if self.logo != None and self.logo != "":
    #         foto = get_thumbnailer(self.logo)['avatar'].url
    #         return format_html('<a href="%s" data-lity data-lity-desc="%s %s"><img src="%s"  width="80" ></a>'%(self.logo.url,self.nombre,self.nit,foto))
    #     else:
    #         return format_html("<p><b>Sin Logo</b></p>")
    # get_foto.short_description = 'Logo'

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'

class Taller(models.Model):
    nombre = models.CharField(verbose_name="Nombre del taller", max_length=100, unique=True)
    correo=models.EmailField(max_length=255,verbose_name="Correo Electronico")
    telefono=models.PositiveIntegerField(verbose_name="Telefono")
    direccion = models.CharField(verbose_name="Direccion", max_length=100)

    nombre_contacto = models.CharField(max_length=150, verbose_name='Nombre de contacto', blank=True, null=True)
    telefono_contacto = models.CharField(max_length=50, verbose_name='Telefono de contacto', blank=True, null=True)
    email_contacto = models.EmailField(max_length=255, verbose_name='Correo Electronico del contacto', blank=True, null=True)
    celular_contacto = models.CharField(max_length=100, verbose_name='Celular del contacto', blank=True, null=True)

    nuw_departamento_fk = models.ForeignKey("localizacion.departamento", verbose_name='Departamento', blank=True, null=True)
    municipio_fk = ChainedForeignKey(
        'localizacion.municipio',
        chained_field="nuw_departamento_fk",
        chained_model_field="departamento_fk",
        show_all=False,
        auto_choose=True, 
        verbose_name="Municipio",
        blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = u'Taller'
        verbose_name_plural = u'Talleres'

class proveedores(models.Model):
    nit_proveedor = models.CharField(max_length=50, verbose_name='N.I.T.', unique=True)
    nombre_proveedor = models.CharField(max_length=255,verbose_name="Proveedor")
    encargado = models.CharField(max_length=255,verbose_name="Jefe de area", blank=True, null=True)
    correo_proveedor = models.EmailField(max_length=255,verbose_name="Correo Electronico", blank=True, null=True)
    telefono1 = models.CharField(max_length=255,verbose_name="Telefono 1", blank=True, null=True)
    telefono2 = models.CharField(max_length=255,verbose_name="Telefono 2", blank=True, null=True)
    direccion = models.CharField(max_length=255,verbose_name="Direccion", blank=True, null=True)
    
    contacto_proveedor = models.CharField(max_length=150, verbose_name='Nombre de contacto', blank=True, null=True)
    telefono_contacto = models.CharField(max_length=50, verbose_name='Telefono de contacto', blank=True, null=True)
    email_contacto = models.EmailField(max_length=255, verbose_name='Correo Electronico del contacto', blank=True, null=True)
    celular_contacto = models.CharField(max_length=100, verbose_name='Celular del contacto', blank=True, null=True)

    nuw_departamento_fk = models.ForeignKey("localizacion.departamento", verbose_name='Departamento', blank=True, null=True)
    municipio_fk = ChainedForeignKey(
        'localizacion.municipio',
        chained_field="nuw_departamento_fk",
        chained_model_field="departamento_fk",
        show_all=False,
        auto_choose=True, 
        verbose_name="Municipio",
        blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.nombre_proveedor

    class Meta:
        verbose_name = u'Proveedor'
        verbose_name_plural = u'Proveedores'

class prenda(models.Model):
    codigoPrenda = models.CharField(verbose_name="Codigo", max_length=150, unique=True)
    tipo_prenda = models.CharField(verbose_name="Tipo prenda", max_length=200, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.tipo_prenda
    
    class Meta:
        verbose_name = u'Prenda'
        verbose_name_plural = u'Prendas'

class materia_prima(models.Model):
    codigoMP = models.CharField(verbose_name="Codigo", max_length=150, unique=True)
    nombre = models.CharField(verbose_name="Materia prima", max_length=100, unique=True)
    composicion = models.TextField(verbose_name="Composicion", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        verbose_name = u'Materia Prima'
        verbose_name_plural = u'Materias Primas'

class color(models.Model):
    codigoColor= models.CharField(verbose_name="Codigo", max_length=100)
    color = models.CharField(verbose_name="Color", max_length=100)
    materia_prima_fk = models.ForeignKey(materia_prima, verbose_name="Materia prima")
    proveedor_fk = models.ManyToManyField(proveedores, verbose_name="Proveedor")
    #order = models.PositiveIntegerField(verbose_name="Orden")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return "%s" %(self.color)
    
    class Meta:
        verbose_name = u'Color'
        verbose_name_plural = u'Colores'

class pedido(models.Model):
    CHOICE_ESTADO_PEDIDO = (
        ("pendiente","Pendiente"),
        ("rechazado","Rechazado"),
        ("aceptado", "Aceptado"),
    )
    num_pedido = models.PositiveIntegerField(verbose_name="Orden de compra", unique=True)
    cliente_fk = models.ForeignKey(clientes, verbose_name="Empresa")
    digitador = models.ForeignKey('usuarios.administradores', verbose_name="Responsable", null=True, blank=True)
    estado = models.CharField(choices=CHOICE_ESTADO_PEDIDO, verbose_name="Estado del pedido", max_length=20)
    fecha_llegada = models.DateField(verbose_name="Fecha Llegada")
    fechaEstimada_entrega = models.DateField(verbose_name="Fecha estimada para entrega")
    modelo_orden=models.FileField(verbose_name="Modelo de orden", upload_to="uploads/pedidos/ordenes", max_length=100, null=True, blank=True)
    tallaje=models.FileField(verbose_name="Tallaje", upload_to="uploads/pedidos/tallajes", max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")
    #fecha_aceptarOrden = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha aceptada")

    def __unicode__(self):
        return "%s" %(self.num_pedido)
    
    class Meta:
        verbose_name = u'Orden de compra'
        verbose_name_plural = u'Odenes de compra'
    
class Detalle_predido(models.Model):
    CHOICES_TIPO_LOGO = (
        ("estampado", "Estampado"),
        ("bordado", "Bordado"),
    )
    CHOICES_REFLECTIVO = (
        ("si", "Si"),
        ("no", "No"),
    )
    CHOICE_ESTADO_DETPEDIDO = (
        ("programado", "Programado"),
        ("encorte", "En Corte"),
        ("enconfeccion", "En Confeccion"),
        ("endisenologo", "En Diseño de Logo"),
        ("despachado", "Despachado"),
    )
    codigo_pedido = models.CharField(verbose_name="Codigo del Pedido", max_length=100,help_text="Codigo generado automaticamente")
    pedido = models.ForeignKey(pedido, verbose_name="Pedido")
    materia_prima = models.ForeignKey(materia_prima, verbose_name="Materia prima")
    prenda = models.ForeignKey(prenda, verbose_name="Prenda")
    color = models.ForeignKey(color, verbose_name="Color")
    # ChainedForeignKey(
    #             color,
    #             chained_field="materia_prima",
    #             chained_model_field="materia_prima_fk",
    #             show_all=False,
    #             auto_choose=True, 
    #             verbose_name="Color")
    logo = models.ImageField(verbose_name="Logo", upload_to="uploads/pedidos/logos", null=True, blank=True)
    diseno = models.ImageField(verbose_name="Diseño de prenda", upload_to="uploads/pedidos/diseño_prenda", null=True, blank=True)
    tipo_logo = models.CharField(verbose_name="Tipo de logo", choices=CHOICES_TIPO_LOGO, max_length=20, null=True, blank=True)
    ubicacion_logo = models.CharField(verbose_name="Ubicacion del logo", max_length=100, null=True, blank=True)
    reflectivo = models.CharField(choices=CHOICES_REFLECTIVO, verbose_name="Reflectivo", max_length=100, null=True, blank=True, default='no')
    ubicacion_reflectivo = models.CharField(verbose_name="Ubicacion reflectivo", max_length=100, null=True, blank=True)
    observaciones_pedido = models.TextField(verbose_name="Observaciones del pedido", null=True, blank=True)
    

    estado = models.CharField(choices=CHOICE_ESTADO_DETPEDIDO, verbose_name="Estado", max_length=100)

    fecha_en_corte_inicio = models.DateField(verbose_name="Fecha inicio corte", null=True, blank=True)
    fecha_en_corte_fin = models.DateField(verbose_name="Fecha finalizacion corte", null=True, blank=True)
    fecha_en_confeccion_incio = models.DateField(verbose_name="Fecha inicio confeccion", null=True, blank=True)
    fecha_en_confeccion_fin = models.DateField(verbose_name="Fecha finalizacion confeccion", null=True, blank=True)
    fecha_en_diseno_logo_inicio = models.DateField(verbose_name="Fecha inicio diseño de logo", null=True, blank=True)
    fecha_en_diseno_logo_fin = models.DateField(verbose_name="Fecha finalizacion diseño de logo", null=True, blank=True)
    
    promedioPrenda = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Promedio de prenda")
    observaciones = models.TextField(verbose_name="Observaciones", null=True, blank=True, help_text="Observaciones para correccion del pedido")
    observacionesProduccion = models.TextField(verbose_name="Observaciones para produccion", null=True, blank=True, help_text="Observaciones para produccion")
    order = models.PositiveIntegerField(verbose_name="Orden")
    cant_asig_mp = models.DecimalField(max_digits=100, decimal_places=0,verbose_name="Cantidad de tela asignada (m)",null=True,blank=True,default=Decimal('0.00'))
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def ver_foto_admin(self):
		try:
			photo = get_thumbnailer(self.logo)['avatar'].url
		except Exception, e:
			photo = None
		
		if(photo!=None and photo!=""):
			return format_html('<img src="%s"  width="150" >'%(photo))
		else:
			return format_html('<b>Sin Logo</b>')
    ver_foto_admin.short_description='Logo guardado'

    def ver_diseno_admin(self):
		try:
			photo = get_thumbnailer(self.diseno)['avatar'].url
		except Exception, e:
			photo = None
		
		if(photo!=None and photo!=""):
			return format_html('<img src="%s"  width="150" >'%(photo))
		else:
			return format_html('<b>Sin Diseño de Prenda</b>')
    ver_diseno_admin.short_description='Diseño de prenda guardado'

    def file_link(self):
        if self.pedido.modelo_orden:
            return "<a href='%s'>Descargar</a>" %(self.pedido.modelo_orden.url,)
        else:
            return "Sin orden"
    file_link.allow_tags = True
    file_link.short_description='Orden de Compra'

    def __unicode__(self):
        return "%s" %(self.codigo_pedido)
    
    class Meta:
        verbose_name = u'Pedido'
        verbose_name_plural = u'Pedidos'

class configuracion_talla_detpedido(models.Model):
    pedido_fk = models.ForeignKey(pedido, verbose_name="Pedido")
    detalle_pedido_fk = ChainedForeignKey(
                        Detalle_predido,
                        chained_field="pedido_fk",
                        chained_model_field="pedido",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Pedido")
    talla_fk = models.CharField(max_length=50,verbose_name="Talla")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    taller_fk = models.ForeignKey(Taller, verbose_name="Taller", null=True, blank=True)
    order = models.PositiveIntegerField(verbose_name="Orden")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")

    def __unicode__(self):
        return "%s" %(self.talla_fk)
    
    class Meta:
        verbose_name = u'Configuracion talla pedido'
        verbose_name_plural = u'Configuracion tallas pedidos'

class Ficha_tecnica_detalle_confeccion(models.Model):
    pedido_fk = models.ForeignKey(pedido, verbose_name="Pedido")
    detalle_pedido_fk = ChainedForeignKey(
                        Detalle_predido,
                        chained_field="pedido_fk",
                        chained_model_field="pedido",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Pedido")
    dotacion = models.CharField(verbose_name="Dotacion", max_length=200, null=True, blank=True)
    pes_puntes = models.CharField(verbose_name="Pespuntes", max_length=200, null=True, blank=True)
    ojales = models.CharField(verbose_name="Ojales", max_length=200, null=True, blank=True)
    bolsillo = models.CharField(verbose_name="Bolsillo", max_length=200, null=True, blank=True)
    sobrehilo = models.CharField(verbose_name="Sobrehilo", max_length=200, null=True, blank=True)
    puntadas = models.CharField(verbose_name="Puntadas", max_length=200, null=True, blank=True)
    color_hilo = models.CharField(verbose_name="Color de hilo", max_length=200, null=True, blank=True)
    dobladillos = models.CharField(verbose_name="Dobladillos", max_length=200, null=True, blank=True)
    amarres = models.CharField(verbose_name="Amarres", max_length=200, null=True, blank=True)
    recubridora = models.CharField(verbose_name="Recubridora", max_length=200, null=True, blank=True)
    bies = models.CharField(verbose_name="Bies", max_length=200, null=True, blank=True)
    color_recubridora = models.CharField(verbose_name="Color", max_length=200, null=True, blank=True)
    entre_tela = models.CharField(verbose_name="Entretela", max_length=200, null=True, blank=True)
    tono = models.CharField(verbose_name="Tono", max_length=200, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")
    order = models.PositiveIntegerField(verbose_name="Orden")

    def __unicode__(self):
        return "%s" %(self.detalle_pedido_fk)

    class Meta:
        verbose_name = u'Detalle de confeccion'
        verbose_name_plural = u'Detalle de confecciones'

class Ficha_tecnica_detalle_insumo(models.Model):
    pedido_fk = models.ForeignKey(pedido, verbose_name="Pedido")
    detalle_pedido_fk = ChainedForeignKey(
                        Detalle_predido,
                        chained_field="pedido_fk",
                        chained_model_field="pedido",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Pedido")
    botones = models.CharField(verbose_name="Botones", max_length=200, null=True, blank=True)
    zipper = models.CharField(verbose_name="Zipper", max_length=200, null=True, blank=True)
    ubicacion = models.CharField(verbose_name="Ubicacion Bolsillo", max_length=200, null=True, blank=True)
    remaches = models.CharField(verbose_name="Remaches", max_length=200, null=True, blank=True)
    elastico = models.CharField(verbose_name="Elastico", max_length=200, null=True, blank=True)
    ubicacion_remache = models.CharField(verbose_name="Ubicacion Remache", max_length=200, null=True, blank=True)
    tallin = models.CharField(verbose_name="Tallin", max_length=200, null=True, blank=True)
    garra = models.CharField(verbose_name="Garra", max_length=200, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")
    order = models.PositiveIntegerField(verbose_name="Orden")

    def __unicode__(self):
        return "%s" %(self.detalle_pedido_fk)

    class Meta:
        verbose_name = u'Detalle de insumo'
        verbose_name_plural = u'Detalle de insumos'

class Ficha_tecnica_detalle_costo(models.Model):
    pedido_fk = models.ForeignKey(pedido, verbose_name="Pedido")
    detalle_pedido_fk = ChainedForeignKey(
                        Detalle_predido,
                        chained_field="pedido_fk",
                        chained_model_field="pedido",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Pedido")
    costoCorte = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de Corte", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoConfeccion = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de Confeccion", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costologo = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de diseño de logo", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoFlete = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de flete", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoMateriaPrima = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo materia prima", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoAdicional = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costos adicionales", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoFleteEntrada = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de flete en entrada", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    costoFleteDespacho = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo de flete para despacho", null=True, blank=True, help_text="en mano de Obra (Unitario)")
    descripcioncostoAdicional = models.CharField( verbose_name="Descripcion de Costos Adicionales", max_length=200, null=True, blank=True)

    total_prenda = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo total por prenda", null=True, blank=True)
    total_pedido = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Costo total por pedido", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Fecha creacion")
    order = models.PositiveIntegerField(verbose_name="Orden")

    def __unicode__(self):
        return "%s" %(self.detalle_pedido_fk)

    class Meta:
        verbose_name = u'Detalle de costo'
        verbose_name_plural = u'Detalle de costos'



##########################################################################################
class Factura_CompraMP(models.Model):
    fecha_compra = models.DateField(verbose_name="Fecha de compra")#Que el comercial ingrese la fecha
    numeroFacturaMP = models.CharField(verbose_name="Numero de Factura", max_length=200, unique=True)
    precio = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Precio de compra", help_text="Precio de compra por metro")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    descuento = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Descuento", null=True, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=0, verbose_name="Total")
    observaciones = models.TextField(verbose_name="Observaciones", null=True, blank=True)
    facturaMP_fk = models.ForeignKey(materia_prima,verbose_name="Materia Prima", max_length=200)
    facturaMP_Color_fk = ChainedForeignKey(
                        color,
                        chained_field="facturaMP_fk",
                        chained_model_field="materia_prima_fk",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Color")
    proveedor_fk = models.ForeignKey(proveedores, verbose_name="Proveedor")

    def __unicode__(self):
        return self.numeroFacturaMP

    class Meta:
        verbose_name = u'Factura de Compra'
        verbose_name_plural = u'Facturas de Compra'

#-----------------MODELO CONTROL DE MATERIA PRIMA----------
class Control_MateriaPrima(models.Model):
    cantidad_gastada = models.PositiveIntegerField(verbose_name="Cantidad Gastada")
    stock = models.PositiveIntegerField(verbose_name="Cantidad en Stock")
    FacturaCompraMP_fk = models.ForeignKey(Factura_CompraMP, verbose_name="Factura de Compra")
    detallePedidoMP_fk = models.ForeignKey(Detalle_predido, verbose_name="Pedido al que pertenece")

    def __unicode__(self):
        return "%s" %(self.cantidad_gastada)

    class Meta:
        verbose_name = u'Control Materia Prima'
        verbose_name_plural = u'Control de Materia Prima'

#-----------------MODELO -  CONTROL PRENDAS----------
class Control_Prendas(models.Model): 
    controlMP_cliente_fk = models.ForeignKey(clientes, verbose_name="Empresa")
    controlMP_ordenC_fk = ChainedForeignKey(
                            pedido,
                            chained_field="controlMP_cliente_fk",
                            chained_model_field="cliente_fk",
                            show_all=False,
                            auto_choose=False, 
                            verbose_name="Orden de Compra")
    controlMP_Detallepedido_fk = ChainedForeignKey(
                                    Detalle_predido,
                                    chained_field="controlMP_ordenC_fk",
                                    chained_model_field="pedido",
                                    show_all=False,
                                    auto_choose=False, 
                                    verbose_name="Pedido")
    talla = ChainedForeignKey(
            configuracion_talla_detpedido,
            chained_field="controlMP_Detallepedido_fk",
            chained_model_field="detalle_pedido_fk",
            show_all=False,
            auto_choose=False, 
            verbose_name="Talla")
    #models.CharField(verbose_name="Talla", max_length=200)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad entregada")
    cantidad_pendiente = models.PositiveIntegerField(verbose_name="Cantidad para despacho",null=True,blank=True)
    
    def __unicode__(self):
        return "%s" %(self.controlMP_ordenC_fk)

    class Meta:
        verbose_name = u'Control de Prendas'
        verbose_name_plural = u'Control de Prendas'

class Inventario_Prendas(models.Model): 
    inventarioPrenda_fk = models.ForeignKey(prenda, verbose_name="Prenda")
    inventarioMP_fk = models.ForeignKey(materia_prima, verbose_name="Materia Prima")
    inventarioColor_fk = ChainedForeignKey(
                        color,
                        chained_field="inventarioMP_fk",
                        chained_model_field="materia_prima_fk",
                        show_all=False,
                        auto_choose=True, 
                        verbose_name="Color")
    talla = models.CharField(verbose_name="Talla", max_length=200)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")

    def __unicode__(self):
        return "%s" %(self.inventarioPrenda_fk)
    
    class Meta:
        verbose_name = u'Inventario de Prendas'
        verbose_name_plural = u'Inventario de Prendas'

class Inventario_materia_prima(models.Model): 
    materia_prima_fk = models.ForeignKey(materia_prima, verbose_name="Materia prima")
    color_fk = ChainedForeignKey(
                        color,
                        chained_field="materia_prima_fk",
                        chained_model_field="materia_prima_fk",
                        show_all=False,
                        auto_choose=False, 
                        verbose_name="Color")
    cantidad = models.PositiveIntegerField(verbose_name="Stock")

    def __unicode__(self):
        return "%s" %(self.materia_prima_fk)
    
    class Meta:
        verbose_name = u'Inventario de materia prima'
        verbose_name_plural = u'Inventario de materias primas'