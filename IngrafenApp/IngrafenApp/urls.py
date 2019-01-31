"""IngrafenApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cotizacion import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("solicitud/", views.solicitud_cot, name="solicitud"),
    path("registro/",views.creacion_usuario, name="creacion_usuario"),
    path("login/",views.user_login,name="login"),
    path("logout/", views.user_logout,name="logout"),
    path("solicitudes/",views.solicitudes_existentes, name="solicitudes_existentes"),
    path("cotizacion/",views.cotizaciones_completadas, name="cotizaciones_completadas"),
    path("crear_material/",views.creacion_material,name="crear_material"),
    path("crear_cliente/",views.creacion_cliente,name="crear_cliente"),
    path("crear_trabajo/",views.creacion_trabajo,name="crear_trabajo"),
    path("contactenos/",views.contactenos,name="contactenos"),
    path("compañia/", views.quienes_somos,name="quienes_somos"),
    path("servicios/",views.servicios,name="servicios"),
    path("reportes/",views.reportes,name="reportes"),
    path("solicitud_ot/",views.solicitud_ot,name="solicitud_ot"),
    path("ordenes_por_aperturar/",views.ordenes_por_aperturar,name="ordenes_por_aperturar"),
    path("ordenes_aperturadas/",views.ordenes_aperturadas,name="ordenes_aperturadas"),
    path("ordenes_en_proceso/",views.ordenes_en_proceso,name="ordenes_en_proceso"),
    path("ordenes_sin_fecha/",views.ordenes_sin_fecha,name="ordenes_sin_fecha"),
    path("error01/",views.error01,name="error01"),
    path("clientes_ot/",views.creacion_cliente_ot,name="creacion_cliente_ot"),
    path("bloqueo_clientes/",views.bloqueo_clientes,name="bloqueo_clientes"),
    path("confirmacion_material/",views.confirmacion_material,name="confirmacion_material"),
    path("cambio_contraseña/",views.change_password,name="cambio_contraseña"),
    path("eliminar_solicitud/",views.eliminar_solicitud,name="eliminar_solicitud"),
    path("solicitud_gigantografia",views.solicitud_gigantografia,name="solicitud_gigantografia"),
    path("crear_material_gig",views.creacion_material_gig,name="crear_material_gig"),
    path("crear_trabajo_gig",views.creacion_trabajo_gig,name="crear_trabajo_gig"),
    path("ordenes_por_aperturar_gig",views.ordenes_por_aperturar_gig,name="ordenes_por_aperturar_gig"),
    path("ordenes_en_proceso_gig/",views.ordenes_en_proceso_gig,name="ordenes_en_proceso_gig"),
    path("ordenes_sin_fecha_gig/",views.ordenes_sin_fecha_gig,name="ordenes_sin_fecha_gig"),
<<<<<<< HEAD
    path("ordenes_aperturadas_gig/",views.ordenes_aperturadas_gig,name="ordenes_aperturadas_gig"),
=======
>>>>>>> 6006d8a93f57e0c347be39fe52a2e53416a1908b


]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
