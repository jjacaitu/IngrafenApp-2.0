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


]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
