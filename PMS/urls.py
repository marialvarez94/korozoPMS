"""PMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from prendas import views
from django.contrib.auth.views import login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = [
    #url(r'^users/$', views.users),
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^admin/programacion/$', views.calendario_view),
    url(r'^detalle-orden/$', views.detalle_programacion_orden_compra),
    url(r'^programacion/', views.programacion),
    url(r'^prueba/', views.imprimir_orden_corte),
    url(r'^orden-confeccion/', views.imprimir_orden_confeccion),
    url(r'^orden-logo/', views.imprimir_orden_logo),
    url(r'^inventario-materia-prima/', views.buscar_inv_materia_prima),
    url(r'^asignacion-materia-prima/', views.asignacion_materia_prima),
    url(r'^inventario-prenda/', views.buscar_inv_prenda),
    url(r'^asignacion-prenda/', views.asignacion_prenda),
    
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),

    url(r'^reset/password_reset', password_reset, {'template_name':'registration/password_reset_form.html', 'email_template_name':'registration/password_reset_email.html','html_email_template_name':'registration/password_reset_email_html.html','subject_template_name':'registration/subject_email.txt'}, name="password_reset"),   
    url(r'^account/password_reset_done', password_reset_done, {'template_name':'registration/password_reset_done.html'}, name="password_reset_done"),    
    url(r'^account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name':'registration/password_reset_confirm.html'}, name="password_reset_confirm"),
    url(r'^account/password_reset_complete', password_reset_complete, {'template_name':'registration/password_reset_complete.html'}, name="password_reset_complete"),   

]
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  