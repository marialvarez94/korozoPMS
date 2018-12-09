from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import *
from decimal import *


# Create your views here.
@staff_member_required
def calendario_view(request):
    """
    If you're using multiple admin sites with independent views you'll need to set
    current_app manually and use correct admin.site
    # request.current_app = 'admin'
    """
    json = []
    if len(request.user.groups.all()) > 0:
        if request.user.groups.all()[0].name == 'COMERCIANTE':
            comerciante = request.user.pk
            orden_obj = pedido.objects.filter(digitador__pk = comerciante, estado = 'aceptado')
            for orden in orden_obj:
                ordenDir = {}
                titulo = "%s - %s" %(orden.num_pedido, orden.cliente_fk.nombre)
                ordenDir['pk'] = orden.num_pedido
                ordenDir['titulo'] = titulo
                json.append(ordenDir)
        elif request.user.groups.all()[0].name == 'EMPRESA':
            empresa = request.user.clientes_fk.nombre
            orden_obj = pedido.objects.filter(cliente_fk__nombre = empresa, estado = 'aceptado')
            for orden in orden_obj:
                ordenDir = {}
                titulo = "%s - %s" %(orden.num_pedido, orden.cliente_fk.nombre)
                ordenDir['pk'] = orden.num_pedido
                ordenDir['titulo'] = titulo
                json.append(ordenDir)
        elif request.user.groups.all()[0].name == 'AUDITOR':
            orden_obj = pedido.objects.filter(estado = 'aceptado')
            for orden in orden_obj:
                ordenDir = {}
                titulo = "%s - %s" %(orden.num_pedido, orden.cliente_fk.nombre)
                ordenDir['pk'] = orden.num_pedido
                ordenDir['titulo'] = titulo
                json.append(ordenDir)
    elif request.user.is_superuser:
        orden_obj = pedido.objects.filter(estado = 'aceptado')
        for orden in orden_obj:
            ordenDir = {}
            titulo = "%s - %s" %(orden.num_pedido, orden.cliente_fk.nombre)
            ordenDir['pk'] = orden.num_pedido
            ordenDir['titulo'] = titulo
            json.append(ordenDir)
    
    context = admin.site.each_context(request)
    context.update({
        'title': 'Programacion',
        'ordenes':json,
    })

    template = 'admin/calendario.html'
    return render(request, template, context)

@login_required(login_url="/admin")
@csrf_exempt
def programacion(request):
    try:
        orden_pk = request.POST['pk']
        pedido_obj = pedido.objects.get(num_pedido = orden_pk)
        detalle_obj = Detalle_predido.objects.filter(pedido = pedido_obj)
        json = []
        detDir = {}

        fin = str(pedido_obj.fechaEstimada_entrega)
        titulo = "Orden de compra %s para la empresa %s" %(pedido_obj.num_pedido, pedido_obj.cliente_fk)
        detDir['id'] = pedido_obj.pk
        detDir["title"] = titulo
        detDir['start'] = pedido_obj.fecha_llegada
        detDir['end'] = fin+"T18:00:00"
        json.append(detDir)
        for det in detalle_obj:
            detDir = {}
            if det.estado == 'encorte':
                fin_corte = str(det.fecha_en_corte_fin)
                detDir["title"] = "Codigo de pedido "+det.codigo_pedido
                detDir['start'] = det.fecha_en_corte_inicio
                detDir['end'] = fin_corte+"T18:00:00"
                detDir['color'] = '#DD2121'
            elif det.estado == 'enconfeccion':
                fin_confeccion = str(det.fecha_en_confeccion_fin)
                detDir["title"] = "Codigo de pedido "+det.codigo_pedido
                detDir['start'] = det.fecha_en_confeccion_incio
                detDir['end'] = fin_confeccion+"T18:00:00"
                detDir['color'] = '#FE9A2E'
            elif det.estado == 'endisenologo':
                fin_logo = str(det.fecha_en_diseno_logo_fin)
                detDir["title"] = "Codigo de pedido "+det.codigo_pedido
                detDir['start'] = det.fecha_en_diseno_logo_inicio
                detDir['end'] = fin_logo+"T18:00:00"
                detDir['color'] = '#4B8A08'
            else:
                pass
            json.append(detDir)
        return JsonResponse(json, safe=False)
    except:
        return HttpResponse("Error")

@login_required(login_url="/admin")
@csrf_exempt
def detalle_programacion_orden_compra(request):
    if request.method == 'POST':
        pk_event = request.POST['pk']
        orden_compra_obj = pedido.objects.get(pk = pk_event)
        json_pedido = []

        ordenDir = {}
        nom_ape_digitador = "%s %s" %(orden_compra_obj.digitador.last_name, orden_compra_obj.digitador.first_name)
        ordenDir['num_pedido'] = orden_compra_obj.num_pedido
        ordenDir['cliente_fk'] = orden_compra_obj.cliente_fk.nombre
        ordenDir['digitador'] = nom_ape_digitador
        ordenDir['estado'] = orden_compra_obj.estado
        
        json_pedido.append(ordenDir)
        return JsonResponse(json_pedido, safe=False)
    else:
        return HttpResponse("Error")

@csrf_exempt
def imprimir_orden_corte(request):
    if request.method == 'GET':
        detalle_pk = request.GET['pk']
        detalle_obj = Detalle_predido.objects.get(pk = detalle_pk)
        codigo = detalle_obj.codigo_pedido
        pedido = detalle_obj.pedido.num_pedido
        materia_prima = detalle_obj.materia_prima.nombre
        prenda = detalle_obj.prenda.tipo_prenda
        empresa = detalle_obj.pedido.cliente_fk.nombre
        fecha_llegada = detalle_obj.fecha_en_corte_inicio
        fechaEstimada_entrega = detalle_obj.fecha_en_corte_fin
        promedio_prenda = detalle_obj.promedioPrenda
        color = detalle_obj.color.color
        composicion = detalle_obj.materia_prima.composicion
        observaciones = detalle_obj.observaciones_pedido
        observacionesProduccion = detalle_obj.observacionesProduccion

        dotacion = None
        try:
            dotacion_obj = Ficha_tecnica_detalle_confeccion.objects.get(detalle_pedido_fk__pk = detalle_pk)
            dotacion = dotacion_obj.dotacion
        except:
            pass
        proveedor = detalle_obj.color.proveedor_fk.all()
        provee = []
        for pro in proveedor:
            provee.append(pro.nombre_proveedor)
        
        talla_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__pk = detalle_pk)
        tallas = []
        total = 0.00
        for talla in talla_obj:
            tallaDir = {}
            tallaDir['talla'] = talla.talla_fk
            tallaDir['cantidad'] = talla.cantidad
            tallas.append(tallaDir)
        for i in tallas:
            total += i['cantidad']



        #Cantidad requerida
        prom_tela = 0
        tela = 0
        try:
            prom_tela = detalle_obj.promedioPrenda
        except:
            pass

        #get cantidad de prendas
        detalle_pk2 = detalle_obj.codigo_pedido
        cantidad_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__codigo_pedido = detalle_pk2)
        
        for cant in cantidad_obj:
            tela += cant.cantidad

        cantidad_comprar = tela * prom_tela

        Context = {
            'detalle_obj':detalle_obj,
            'codigo':codigo,
            'pedido':pedido,
            'materia_prima':materia_prima,
            'prenda':prenda,
            'empresa':empresa,
            'llega':fecha_llegada,
            'entrega':fechaEstimada_entrega,
            'promedio_prenda':promedio_prenda,
            'color':color,
            'composicion':composicion,
            'proveedor':provee,
            'talla_cantidad':tallas,
            'total':total,
            'observaciones':observaciones,
            'observacionesProduccion':observacionesProduccion,
            'dotacion':dotacion,
            'cant_comprar':cantidad_comprar,
        }
        html_template = get_template('templates_pdf/orden_compra.html')
        rendered_html = html_template.render(RequestContext(request, Context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(string='@page { size: Letter; }')])
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename=Orden_Corte.pdf'
        return http_response


def imprimir_orden_confeccion(request):
    if request.method == 'GET':
        detalle_pk = request.GET['pk']
        detalle_obj = Detalle_predido.objects.get(pk = detalle_pk)
        codigo = detalle_obj.codigo_pedido
        pedido = detalle_obj.pedido.num_pedido
        materia_prima = detalle_obj.materia_prima.nombre
        prenda = detalle_obj.prenda.tipo_prenda
        empresa = detalle_obj.pedido.cliente_fk.nombre
        fecha_llegada = detalle_obj.fecha_en_confeccion_incio
        fechaEstimada_entrega = detalle_obj.fecha_en_confeccion_fin
        color = detalle_obj.color.color
        observaciones = detalle_obj.observaciones_pedido
        dotacion = None
        Pespuntes = None
        ojales = None
        bolsillo = None
        sobrehilo = None
        puntadas = None
        color_hilo = None
        dobladillos = None
        amarres = None
        recubridora = None
        bies = None
        color_recubridora = None
        entre_tela = None
        tono = None
        #insumos
        botones = None
        zipper = None
        ubicacion = None
        remaches = None
        elastico = None
        ubicacion_remache = None
        tallin = None
        garra = None
        try:
            dotacion_obj = Ficha_tecnica_detalle_confeccion.objects.get(detalle_pedido_fk__pk = detalle_pk)
            dotacion = dotacion_obj.dotacion
            Pespuntes = dotacion_obj.pes_puntes
            ojales = dotacion_obj.ojales
            bolsillo = dotacion_obj.bolsillo
            sobrehilo = dotacion_obj.sobrehilo
            puntadas = dotacion_obj.puntadas
            color_hilo = dotacion_obj.color_hilo
            dobladillos = dotacion_obj.dobladillos
            amarres = dotacion_obj.amarres
            recubridora = dotacion_obj.recubridora
            bies = dotacion_obj.bies
            color_recubridora = dotacion_obj.color_recubridora
            entre_tela = dotacion_obj.entre_tela
            tono = dotacion_obj.tono
        except:
            pass

        try:
            insumo_obj = Ficha_tecnica_detalle_insumo.objects.get(detalle_pedido_fk__pk = detalle_pk)            
            botones = insumo_obj.botones
            zipper = insumo_obj.zipper
            ubicacion = insumo_obj.ubicacion
            remaches = insumo_obj.remaches
            elastico = insumo_obj.elastico
            ubicacion_remache = insumo_obj.ubicacion_remache
            tallin = insumo_obj.tallin
            garra = insumo_obj.garra
        except:
            pass
        
        talla_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__pk = detalle_pk)
        tallas = []
        total = 0.00
        for talla in talla_obj:
            tallaDir = {}
            tallaDir['talla'] = talla.talla_fk
            tallaDir['cantidad'] = talla.cantidad
            tallas.append(tallaDir)
        for i in tallas:
            total += i['cantidad']

        Context = {
            'detalle_obj':detalle_obj,
            'codigo':codigo,
            'pedido':pedido,
            'materia_prima':materia_prima,
            'prenda':prenda,
            'empresa':empresa,
            'llega':fecha_llegada,
            'entrega':fechaEstimada_entrega,
            'color':color,
            'talla_cantidad':tallas,
            'total':total,
            'observaciones':observaciones,
            'dotacion':dotacion,
            'Pespuntes':Pespuntes,
            'ojales':ojales,
            'bolsillo':bolsillo,
            'sobrehilo':sobrehilo,
            'puntadas':puntadas,
            'color_hilo':color_hilo,
            'dobladillos':dobladillos,
            'amarres':amarres,
            'recubridora':recubridora,
            'bies':bies,
            'color_recubridora':color_recubridora,
            'entre_tela':entre_tela,
            'tono':tono,
            'botones':botones,
            'zipper':zipper,
            'ubicacion':ubicacion,
            'remaches':remaches,
            'elastico':elastico,
            'ubicacion_remache':ubicacion_remache,
            'tallin':tallin,
            'garra':garra,
        }
        html_template = get_template('templates_pdf/orden_confeccion.html')
        rendered_html = html_template.render(RequestContext(request, Context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(string='@page { size: Letter; }')])
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename=Orden_Confeccion.pdf'
        return http_response

def imprimir_orden_logo(request):
    if request.method == 'GET':
        detalle_pk = request.GET['pk']
        detalle_obj = Detalle_predido.objects.get(pk = detalle_pk)
        codigo = detalle_obj.codigo_pedido
        pedido = detalle_obj.pedido.num_pedido
        prenda = detalle_obj.prenda.tipo_prenda
        empresa = detalle_obj.pedido.cliente_fk.nombre
        fecha_llegada = detalle_obj.fecha_en_diseno_logo_inicio
        fechaEstimada_entrega = detalle_obj.fecha_en_diseno_logo_fin
        tipo_logo = detalle_obj.tipo_logo
        ubicacion_logo = detalle_obj.ubicacion_logo
        observaciones = detalle_obj.observaciones_pedido
        dotacion = None
        try:
            dotacion_obj = Ficha_tecnica_detalle_confeccion.objects.get(detalle_pedido_fk__pk = detalle_pk)
            dotacion = dotacion_obj.dotacion
        except:
            pass
        
        talla_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk__pk = detalle_pk)
        tallas = []
        total = 0.00
        for talla in talla_obj:
            tallaDir = {}
            tallaDir['talla'] = talla.talla_fk
            tallaDir['cantidad'] = talla.cantidad
            tallas.append(tallaDir)
        for i in tallas:
            total += i['cantidad']

        Context = {
            'detalle_obj':detalle_obj,
            'codigo':codigo,
            'pedido':pedido,
            'prenda':prenda,
            'empresa':empresa,
            'llega':fecha_llegada,
            'entrega':fechaEstimada_entrega,
            'talla_cantidad':tallas,
            'total':total,
            'observaciones':observaciones,
            'dotacion':dotacion,
            'tipo_logo':tipo_logo,
            'ubicacion':ubicacion_logo,
        }
        html_template = get_template('templates_pdf/orden_logo.html')
        rendered_html = html_template.render(RequestContext(request, Context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(string='@page { size: Letter; }')])
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename=Orden_Logo.pdf'
        return http_response

@csrf_exempt
def buscar_inv_materia_prima(request):
    if request.method == 'GET':
        materia = request.GET['mp']
        color = request.GET['cl']
        materia = materia.upper()
        json = []
        invDir = {}

        try:
            inventario_obj = Inventario_materia_prima.objects.get(materia_prima_fk__pk = materia, color_fk__pk = color)
            invDir['mp'] = inventario_obj.materia_prima_fk.nombre
            invDir['cl'] = inventario_obj.color_fk.color
            invDir['cant'] = inventario_obj.cantidad
            json.append(invDir)      
            return JsonResponse(json, safe=False)
        except:
            return HttpResponse('fallo')

@csrf_exempt
def asignacion_materia_prima(request):
    if request.method == 'POST':
        cantidad = request.POST['cant']
        mat_prima = request.POST['mp']
        color = request.POST['cl']
        pk = request.POST['pk']

        inventario_mp = Inventario_materia_prima.objects.get(materia_prima_fk__pk = mat_prima, color_fk__pk = color)
        inventario_mp.cantidad = inventario_mp.cantidad - Decimal(cantidad)
        inventario_mp.save()

        detalle_obj = Detalle_predido.objects.get(pk = pk)
        print(detalle_obj.cant_asig_mp)
        detalle_obj.cant_asig_mp = detalle_obj.cant_asig_mp + Decimal(cantidad)
        detalle_obj.save()
        return HttpResponse('ok')

@csrf_exempt
def buscar_inv_prenda(request):
    if request.method == 'GET':
        materia = request.GET['mp']
        color = request.GET['cl']
        prenda = request.GET['prenda']
        pk = request.GET['pk']
        materia = materia.upper()
        json = []
        
        inventario_obj = Inventario_Prendas.objects.filter(inventarioMP_fk__pk = materia, inventarioColor_fk__pk = color, inventarioPrenda_fk__pk = prenda)
        detalle_obj = Detalle_predido.objects.get(pk = pk)
        for inv in inventario_obj:
            invDir = {}
            invDir['mp'] = inv.inventarioMP_fk.nombre
            invDir['cl'] = inv.inventarioColor_fk.color
            invDir['pr'] = inv.inventarioPrenda_fk.tipo_prenda
            invDir['talla'] = inv.talla
            invDir['cant'] = inv.cantidad
            invDir['pedido_actual'] = []
            tallas_obj = configuracion_talla_detpedido.objects.filter(detalle_pedido_fk = detalle_obj, talla_fk = inv.talla.upper())
            for pedido in tallas_obj:
                pedidoDir = {}
                pedidoDir['mat_prima'] = pedido.detalle_pedido_fk.materia_prima.nombre
                pedidoDir['color'] = pedido.detalle_pedido_fk.color.color
                pedidoDir['prenda'] = pedido.detalle_pedido_fk.prenda.tipo_prenda
                pedidoDir['tallas'] = pedido.talla_fk
                pedidoDir['cantidad'] = pedido.cantidad
                invDir['pedido_actual'].append(pedidoDir)        
            json.append(invDir)
        if len(json) > 0:
            return JsonResponse(json, safe=False)
        else:
            return HttpResponse('fallo')

@csrf_exempt
def asignacion_prenda(request):
    if request.method == 'POST':
        cantidad = request.POST['cant']
        mat_prima = request.POST['mp']
        color = request.POST['cl']
        prenda = request.POST['pr']
        talla = request.POST['talla']
        pk = request.POST['pk']

        inventario_p = Inventario_Prendas.objects.get(inventarioMP_fk = mat_prima, inventarioColor_fk = color, inventarioPrenda_fk = prenda, talla = talla.upper())
        inventario_p.cantidad = inventario_p.cantidad - Decimal(cantidad)
        inventario_p.save()

        tallas_obj = configuracion_talla_detpedido.objects.get(detalle_pedido_fk__pk = pk, talla_fk = talla.upper())
        tallas_obj.cantidad = tallas_obj.cantidad - int(cantidad)
        tallas_obj.save()
        return HttpResponse('ok')




