from suit.apps import DjangoSuitConfig

from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    HEADER_DATE_FORMAT = 'l, j. F Y',
    menu = (

        ParentItem("Localizacion", children=[
            ChildItem(model='localizacion.departamento'),
            ChildItem(model='localizacion.municipio'),
        ],),

        ParentItem("Contactos Directos", children=[
            ChildItem(model='prendas.clientes'),
            ChildItem(model='prendas.proveedores'),
            ChildItem(model='prendas.taller'),
        ],),

        
        ParentItem('Insumos', children=[
            ChildItem(model='prendas.prenda'),
            ChildItem(model='prendas.materia_prima'),
            ChildItem(model='prendas.color'),
            ChildItem(model='prendas.talla'),
        ],),


        ParentItem(u"Control Interno", children=[
            #ChildItem(model='prendas.control_materiaprima'),
            ChildItem(model='prendas.control_prendas'),
        ],),

        ParentItem(u"Inventario", children=[
            ChildItem(model='prendas.inventario_materia_prima'),
            ChildItem(model='prendas.inventario_prendas'),
        ],),

        ParentItem(u'Facturacion', children=[
            ChildItem(model='prendas.factura_compramp'),
        ],),

        
        ParentItem(u'Pedidos', children=[
            ChildItem(model='prendas.pedido'),
            ChildItem(model='prendas.detalle_predido'),
        ],),


        ParentItem('Personal Interno', children=[
            ChildItem('Usuarios', 'usuarios.administradores'),
            ChildItem('Roles', 'auth.group'),
        ], align_right=True,),

        ParentItem(u'Programacion', children=[
            ChildItem('Programacion', url='/admin/programacion/'),
        ],),
        
    )

    def ready(self):
        super(SuitConfig, self).ready()

        # DO NOT COPY FOLLOWING LINE
        # It is only to prevent updating last_login in DB for demo app
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)