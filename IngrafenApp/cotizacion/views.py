from django.shortcuts import render
from cotizacion.forms import Crear_usuario, Solicitud_cot, Materiales, Clientes, TipoDeTrabajo, Solicitud_ot, Solicitud_ot_aprobacion, Clientes_ot, TipoDeTrabajo_gig, Materiales_gig, Solicitud_ot_gig #Bloqueo_cliente
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cotizacion.models import CotizacionesSolicitadas, OrdenesSolicitadas, OrdenesGigantografia
from datetime import datetime, timedelta, date
from cotizacion import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from fusioncharts import FusionCharts
from collections import OrderedDict
from django.http import JsonResponse
from dateutil.relativedelta import *
from calendar import monthrange
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def ordenes_aperturadas_gig(request):
    ver = False
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    clientes_creados = models.Clientes_ot.objects.all().order_by("nombre_razon_social")
    trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
    vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
    tipo_busqueda = ""
    if request.method == "GET" and request.user.categoria == "VEN":
        ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("tipo_busqueda"):

        desde = request.POST.get("desde")
        hasta = request.POST.get("hasta")
        print("AQUIIII",desde,hasta)
        if request.user.categoria == "VEN":
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "Trabajo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.all().filter(tipo_trabajo_ot=request.POST.get("busqueda")).filter(vendedor_ot=request.user).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("busqueda"))
                ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")



            elif request.POST.get("tipo_busqueda") == "Solicitud":
                ordenes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=request.POST.get("busqueda")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Orden":
                ordenes = OrdenesGigantografia.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("busqueda")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Orden"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                ordenes = OrdenesGigantografia.objects.all().filter(trabajo_ot__istartswith=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        else:
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "trabajo_ot"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.all().filter(tipo_trabajo_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("busqueda"))
                ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Vendedor":
                tipo_busqueda = "Vendedor"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.all().filter(vendedor_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cotizador":
                tipo_busqueda = "Cotizador"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesGigantografia.objects.all().filter(cotizador_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Solicitud":
                ordenes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=request.POST.get("busqueda")).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Orden":
                ordenes = OrdenesGigantografia.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("busqueda")).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Orden"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                ordenes = OrdenesGigantografia.objects.all().filter(trabajo_ot__istartswith=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        paginator = Paginator(ordenes,10)
        if request.POST.get("boton") == "siguiente":
            page = request.POST.get("pagina_siguiente")
        else:
            page = request.POST.get("pagina_anterior")
        ordenes_completadas = paginator.get_page(page)

        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"busqueda":busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "siguiente":
        if request.user.categoria == "VEN":
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.POST.get("pagina_siguiente")
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "anterior":
        if request.user.categoria == "VEN":
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.POST.get("pagina_anterior")
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes = OrdenesGigantografia.objects.all().filter(vendedor_ot=request.user).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        print("aqui")
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        print("prueba")

        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("buscar") == "BUSCAR":
        if request.user.categoria == "VEN":
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cl"))
                    ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    ordenes = OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    ordenes = OrdenesGigantografia.objects.all().filter(tipo_trabajo_ot=request.POST.get("tr")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")
                    ordenes = OrdenesGigantografia.objects.all().filter(vendedor_ot=request.POST.get("ven")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    ordenes = OrdenesGigantografia.objects.all().filter(cotizador_ot=request.POST.get("cot")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Solicitud":
                    ordenes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=request.POST.get("parametro")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Orden":
                    ordenes = OrdenesGigantografia.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("parametro")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Orden"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesGigantografia.objects.all().filter(trabajo_ot__istartswith=request.POST.get("parametro")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                print("si")
                clientes_creados = models.Clientes_ot.objects.all().order_by("nombre_razon_social")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(ordenes,10)
                page = request.GET.get('page')
                ordenes_completadas = paginator.get_page(page)
                return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})

        else:
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cl"))
                    ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    ordenes = OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    ordenes = OrdenesGigantografia.objects.all().filter(tipo_trabajo_ot=request.POST.get("tr")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")

                    ordenes = OrdenesGigantografia.objects.all().filter(vendedor_ot=request.POST.get("ven")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    ordenes = OrdenesGigantografia.objects.all().filter(cotizador_ot=request.POST.get("cot")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Solicitud":
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=request.POST.get("parametro")).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Orden":
                    tipo_busqueda = "Orden"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesGigantografia.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("parametro")).order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesGigantografia.objects.all().filter(trabajo_ot__istartswith=request.POST.get("parametro")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                print("si")
                clientes_creados = models.Clientes.objects.all().order_by("nombre")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(ordenes,10)
                page = request.GET.get('page')
                ordenes_completadas = paginator.get_page(page)
                return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})
    if request.method == "POST" and request.POST.get("ver") == "ver orden":
        ver = True

        orden_buscada = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=request.POST.get("cot_ver"))
        return render(request, "ordenes_aperturadas_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_buscada":orden_buscada,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})


    if request.method == "POST" and request.POST.get("regresar") == "REGRESAR":
        ver = False
        if request.user.categoria == "VEN":
            ordenes = OrdenesGigantografia.objects.all().filter(vendedor_ot=request.user).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesGigantografia.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR":
        cot = request.POST.get("cot_reutilizar")
        request.session['cot'] = cot

        return HttpResponseRedirect(reverse('Solicitud_ot_gig'))


@login_required
def ordenes_en_proceso_gig(request):
    buscar = False
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    hoy = datetime.today().date()
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    print(hoy)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).order_by("fecha_entrega_ot")
        else:
            ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        print(ordenes_proceso)
        return render(request, "ordenes_en_proceso_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).order_by("fecha_entrega_ot")
        else:
            ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        return render(request, "ordenes_en_proceso_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_terminado") == "ORDEN TERMINADA":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)

        orden.estado_ot = "Orden terminada"
        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso_gig'))

    elif request.method == "POST" and request.POST.get("boton_cerrar") == "CERRAR OT":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)

        orden.estado_ot = "Cerrada"
        orden.fecha_entregada = date.today()

        orden.fecha_entregada = datetime.now()





        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso_gig'))
    elif request.method == "POST" and request.POST.get("boton_parcial") == "ENTREGA PARCIAL":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)

        if orden.estado_ot == "Orden aperturada" or orden.estado_ot == "Orden terminada":
            orden.estado_ot = "Parcial entregado: " + str(request.POST.get("cantidad_entregada"))

            orden.fecha_entregada = date.today()

            orden.fecha_entregada = datetime.now()

        else:
            cantidad_parcial = orden.estado_ot.split()
            cantidad_calculada = int(cantidad_parcial[-1]) + int(request.POST.get("cantidad_entregada"))
            orden.estado_ot = "Parcial entregado: " + str(cantidad_calculada)

            orden.fecha_entregada = date.today()

            orden.fecha_entregada = datetime.now()








        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso_gig'))

        #return render(request,"ordenes_en_proceso.html",{"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"orden_completada":orden_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")

        orden_existentes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_a_ver)
        return render(request, "ordenes_en_proceso_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})



@login_required
def ordenes_sin_fecha_gig(request):
    buscar = False
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    hoy = datetime.today().date()
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        else:
            ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        print(ordenes_por_fecha)
        return render(request, "ordenes_sin_fecha_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        else:
            ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        return render(request, "ordenes_sin_fecha_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_fecha") == "ESTABLECER FECHA DE ENTREGA":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)

        orden.fecha_entrega_ot = request.POST.get("fecha")





        orden.save()
        return HttpResponseRedirect(reverse('ordenes_sin_fecha_gig'))


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")
        ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        orden_existentes = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_a_ver)
        hoy = datetime.today().date()
        return render(request, "ordenes_sin_fecha_gig.html",{"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})

@login_required
def ordenes_por_aperturar_gig(request):
    buscar = False
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="").filter(vendedor_ot=request.user)
        else:
            ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        print(ordenes_existentes_gig)
        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes_gig":ordenes_existentes_gig,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="").filter(vendedor_ot=request.user)
        else:
            ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes_gig":ordenes_existentes_gig,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_completar") == "COMPLETAR":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden_gig = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)

        orden_gig.fecha_completada_ot = datetime.now()
        orden_gig.cotizador_ot = str(request.user)
        orden_gig.num_ot_relacionada = request.POST.get("orden_papyrus")
        orden_gig.estado_ot = "orden_gig aperturada"
        orden_gig.permiso_borrar = False



        orden_gig.save()

        return HttpResponseRedirect(reverse('ordenes_por_aperturar_gig'))
    elif request.method == "POST" and request.POST.get("asignar") == "ASIGNAR":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes_gig = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        orden_gig = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)
        orden_gig.procesado_por_ot = str(request.user)
        orden_gig.save()

        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes_gig":orden_existentes_gig, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes_gig":ordenes_existentes_gig})
    elif request.method == "POST" and request.POST.get("borrar") == "HABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes_gig = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        orden_gig = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)
        orden_gig.permiso_borrar = True
        orden_gig.save()

        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes_gig":orden_existentes_gig, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes_gig":ordenes_existentes_gig})


    elif request.method == "POST" and request.POST.get("borrar") == "DESHABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes_gig = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        orden_gig = OrdenesGigantografia.objects.get(num_solicitud_ot=numero_1)
        orden_gig.permiso_borrar = False
        orden_gig.save()

        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes_gig":orden_existentes_gig, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes_gig":ordenes_existentes_gig})


        #return render(request,"ordenes_por_aperturar.html",{"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"orden_completada":orden_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")
        ordenes_existentes = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
        orden_existentes_gig = OrdenesGigantografia.objects.all().filter(num_solicitud_ot=numero_a_ver)
        return render(request, "ordenes_por_aperturar_gig.html",{"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes_gig":orden_existentes_gig, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})


@login_required
def creacion_material_gig(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        material = Materiales_gig(data=request.POST)
        if material.is_valid():
            creacion = material.save(commit=False)
            creacion.usuario = request.user
            creacion.material = creacion.material.title()
            creacion.save()
            creado = True
    else:
            material = Materiales_gig()
    return render(request, "materiales_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"material":material, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def creacion_trabajo_gig(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        trabajo = TipoDeTrabajo_gig(data=request.POST)
        if trabajo.is_valid():
            creacion = trabajo.save(commit=False)
            creacion.trabajo = creacion.trabajo.title()
            creacion.usuario = request.user
            creacion.save()
            creado = True
    else:
            trabajo = TipoDeTrabajo_gig()
    return render(request, "tipos_trabajo_gig.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"trabajo":trabajo, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})


def solicitud_gigantografia(request):
    cambiado = False
    aprobada = False
    busqueda = False
    orden = Solicitud_ot_gig(user=request.user)

    solicitado = False
    tipo_trabajo = ""
    materiales = ""
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    numero_solicitud = ""
    tipo_trabajo = models.TipoDeTrabajo_gig.objects.all().order_by("trabajo")
    materiales = models.Materiales_gig.objects.all().order_by("material")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")

    if request.method == "POST" and request.POST.get("Buscar"):
        ot = request.POST.get("ot_reutilizar")
        ver_cinta = ""
        aprobada = False
        try:
            orden_encontrada = models.OrdenesGigantografia.objects.get(num_solicitud_ot = ot)
            cliente_nombre = str(orden_encontrada.nombre_cliente_ot)
            print(cliente_nombre)
            cliente_nombre = cliente_nombre.split()
            del cliente_nombre[0]
            cliente_nombre = " ".join(cliente_nombre)
            cliente_encontrado = models.Clientes_ot.objects.get(nombre_razon_social=cliente_nombre)
            if cliente_encontrado.desactivado == True:
                return HttpResponseRedirect(reverse("error01"))
            print("AQUI",orden_encontrada)
            if orden_encontrada.detalles_ot != "" and orden_encontrada.detalles_ot != None:
                detalle = orden_encontrada.detalles_ot.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto2 = " ".join(texto)
                            orden_encontrada.detalles_ot = texto2
                except:

                    pass




            data = {"nombre_cliente_ot":orden_encontrada.nombre_cliente_ot,"trabajo_ot":orden_encontrada.trabajo_ot,"cantidad_ot":orden_encontrada.cantidad_ot}
            orden = Solicitud_ot(user=request.user,data=data)

        except OrdenesGigantografia.DoesNotExist:
            orden_encontrada = "NO HAY"
            orden = Solicitud_ot_gig(request.user)
        busqueda = True

        tipo_trabajo = models.TipoDeTrabajo_gig.objects.all().order_by("trabajo")
        materiales = models.Materiales_gig.objects.all().order_by("material")


        return render(request, "solicitud_gigantografia.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"cambiado":cambiado,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ver_cinta":ver_cinta,"orden":orden,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"orden_encontrada":orden_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )
    if request.method == 'POST':

        orden = Solicitud_ot_gig(user=request.user,data=request.POST)
        if orden.is_valid():
            print("orden valida")
            stock = orden.save(commit=False)
            stock.vendedor_ot = request.user

            stock.direccion_entrega = request.POST.get("direccion")
            stock.persona_recibe = request.POST.get("persona")
            stock.forma_empaque = request.POST.get("empaque")

            stock.tipo_trabajo_ot = request.POST.get("opciones")
            stock.material_ot = request.POST.get("material1")
            stock.descripcion_material_ot = request.POST.get("descripcion")
            stock.medida_alto_ot = request.POST.get("alto1")
            stock.medida_ancho_ot = request.POST.get("ancho1")

            if request.POST.get("troquel1"):
                stock.troquelado_ot = str(request.POST.get("troquel1"))


            stock.material2_ot = request.POST.get("material2")
            stock.descripcion_material2_ot = request.POST.get("descripcion2")
            if request.POST.get("alto2"):
                stock.medida_alto_2_ot = request.POST.get("alto2")
                stock.medida_ancho_2_ot = request.POST.get("ancho2")
            if request.POST.get("troquel2"):
                stock.troquelado2_ot = str(request.POST.get("troquel2"))

            stock.material3_ot = request.POST.get("material3")
            stock.descripcion_material3_ot = request.POST.get("descripcion3")
            if request.POST.get("alto3"):
                stock.medida_alto_3_ot = request.POST.get("alto3")
                stock.medida_ancho_3_ot = request.POST.get("ancho3")

            if request.POST.get("troquel3"):
                stock.troquelado3_ot = str(request.POST.get("troquel3"))


            stock.material4_ot = request.POST.get("material4")
            stock.descripcion_material4_ot = request.POST.get("descripcion4")
            if request.POST.get("alto4"):
                stock.medida_alto_4_ot = request.POST.get("alto4")
                stock.medida_ancho_4_ot = request.POST.get("ancho4")

            if request.POST.get("troquel4"):
                stock.troquelado4_ot = str(request.POST.get("troquel4"))

            stock.material5_ot = request.POST.get("material5")
            stock.descripcion_material5_ot = request.POST.get("descripcion5")
            if request.POST.get("alto5"):
                stock.medida_alto_5_ot = request.POST.get("alto5")
                stock.medida_ancho_5_ot = request.POST.get("ancho5")

            if request.POST.get("troquel5"):
                stock.troquelado5_ot = str(request.POST.get("troquel5"))


            stock.detalles_ot = ""
            if request.POST.get("cantidad_cintas") != None:

                stock.detalles_ot = str(request.POST.get("cantidad_cintas")) + " pedazos de " + str(request.POST.get("tipo_cinta"))
                stock.detalles_ot += " de " + str(request.POST.get("cm_cintas")) + " cms" + "\n"
            if request.POST.get("adicional"):

                stock.detalles_ot += request.POST.get("adicional") + request.POST.get("adicional_texto")+ "\n"



            stock.detalles_ot += request.POST.get("detalles")



            stock.save()
            solicitado = True
            busqueda = False
            ot_modelo = models.TipoDeTrabajo_gig.objects.all()
            numero_solicitud = models.OrdenesGigantografia.objects.all().last()
            tipo_trabajo = models.TipoDeTrabajo_gig.objects.all().order_by("trabajo")
            materiales = models.Materiales_gig.objects.all().order_by("material")

            return render(request, 'solicitud_gigantografia.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})

    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR ULTIMA ORDEN":
        cot = request.POST.get("cot_reutilizar_ult")
        ver_cinta = ""
        try:
            orden_encontrada = models.OrdenesGigantografia.objects.get(num_solicitud_ot = cot)
            print("AQUI",orden_encontrada)
            data = {"nombre_cliente_ot":orden_encontrada.nombre_cliente_ot,"trabajo_ot":orden_encontrada.trabajo_ot,"cantidad_ot":orden_encontrada.cantidad_ot}
            orden = Solicitud_ot(user=request.user,data=data)
            if orden_encontrada.detalles_ot != "" and orden_encontrada.detalles_ot != None:
                detalle = orden_encontrada.detalles_ot.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto = " ".join(texto)
                            orden_encontrada.detalles_ot = texto
                except:

                    pass





        except OrdenesGigantografia.DoesNotExist:
            orden_encontrada = "NO HAY"
            cotizacion = Solicitud_ot_gig(request.user)
        busqueda = True
        tipo_trabajo = models.TipoDeTrabajo_gig.objects.all().order_by("trabajo")
        materiales = models.Materiales_gig.objects.all().order_by("material")


        return render(request, 'solicitud_gigantografia.html',{"orden_encontrada":orden_encontrada,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"cambiado":cambiado,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})


    else:
        cambiado = False
        orden = Solicitud_ot_gig(user=request.user)
        solicitado = False
        print("AQUI")

        busqueda = False
        ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")

        tipo_trabajo = models.TipoDeTrabajo_gig.objects.all().order_by("trabajo")
        materiales = models.Materiales_gig.objects.all().order_by("material")

        return render(request, 'solicitud_gigantografia.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"cambiado":cambiado,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})




@login_required
def eliminar_solicitud(request):
    cambiado = False
    usuarios_existentes = models.Usuarios.objects.all()
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_eliminar = models.OrdenesSolicitadas.objects.all().filter(permiso_borrar=True)
    cotizaciones_eliminar = models.CotizacionesSolicitadas.objects.all().filter(permiso_borrar=True)
    gig_eliminar = models.OrdenesGigantografia.objects.all().filter(permiso_borrar=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST' and request.POST.get("eliminar_ot"):
        cambiado = True
        orden_a_eliminar = models.OrdenesSolicitadas.objects.get(num_solicitud_ot=request.POST.get("orden"))
        cot_relacionada = models.CotizacionesSolicitadas.objects.get(solicitud_ot=orden_a_eliminar.num_solicitud_ot)
        cot_relacionada.solicitud_ot = ""
        cot_relacionada.save()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_ot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.ordenes_borradas_mes = 0
        usuario.ordenes_borradas_mes += 1
        usuario.ordenes_borradas_totales += 1
        usuario.fecha_ultima_ot = datetime.today()
        usuario.save()
        orden_a_eliminar.delete()
    if request.method == 'POST' and request.POST.get("eliminar_cot"):
        cambiado = True
        cot_a_eliminar = models.CotizacionesSolicitadas.objects.get(num_solicitud=request.POST.get("cotizacion"))
        cot_a_eliminar.delete()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_cot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.cotizaciones_borradas_mes = 0
        usuario.cotizaciones_borradas_mes += 1
        usuario.cotizaciones_borradas_totales += 1
        usuario.fecha_ultima_cot = datetime.today()
        usuario.save()
    if request.method == 'POST' and request.POST.get("eliminar_gig"):
        cambiado = True
        orden_a_eliminar = models.OrdenesGigantografia.objects.get(num_solicitud_ot=request.POST.get("orden_gig"))

        orden_a_eliminar.delete()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_ot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.ordenes_borradas_mes = 0
        usuario.ordenes_borradas_mes += 1
        usuario.ordenes_borradas_totales += 1
        usuario.fecha_ultima_ot = datetime.today()
        usuario.save()
    else:
        cambiado = False

    return render(request, 'eliminar_solicitud.html',{"gig_eliminar":gig_eliminar,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,
        "ordenes_eliminar":ordenes_eliminar,"cotizaciones_eliminar":cotizaciones_eliminar,'cambiado': cambiado,"usuarios_existentes":usuarios_existentes,"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"cotizaciones_existentes":cotizaciones_existentes
    })


@login_required
def change_password(request):
    cambiado = False
    usuarios_existentes = models.Usuarios.objects.all()
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':
        cambiado = True
        u = models.Usuarios.objects.get(username=request.POST.get("usuario"))
        u.set_password(request.POST.get("contraseña"))
        u.save()
    else:
        cambiado = False

    return render(request, 'cambio_contraseña.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,
        'cambiado': cambiado,"usuarios_existentes":usuarios_existentes,"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"cotizaciones_existentes":cotizaciones_existentes
    })





@login_required
def eliminar_solicitud(request):
    cambiado = False
    usuarios_existentes = models.Usuarios.objects.all()
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_eliminar = models.OrdenesSolicitadas.objects.all().filter(permiso_borrar=True)
    cotizaciones_eliminar = models.CotizacionesSolicitadas.objects.all().filter(permiso_borrar=True)
    gig_eliminar = models.OrdenesGigantografia.objects.all().filter(permiso_borrar=True)
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST' and request.POST.get("eliminar_ot"):
        cambiado = True
        orden_a_eliminar = models.OrdenesSolicitadas.objects.get(num_solicitud_ot=request.POST.get("orden"))
        cot_relacionada = models.CotizacionesSolicitadas.objects.get(solicitud_ot=orden_a_eliminar.num_solicitud_ot)
        cot_relacionada.solicitud_ot = ""
        cot_relacionada.save()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_ot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.ordenes_borradas_mes = 0
        usuario.ordenes_borradas_mes += 1
        usuario.ordenes_borradas_totales += 1
        usuario.fecha_ultima_ot = datetime.today()
        usuario.save()
        orden_a_eliminar.delete()
    if request.method == 'POST' and request.POST.get("eliminar_cot"):
        cambiado = True
        cot_a_eliminar = models.CotizacionesSolicitadas.objects.get(num_solicitud=request.POST.get("cotizacion"))
        cot_a_eliminar.delete()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_cot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.cotizaciones_borradas_mes = 0
        usuario.cotizaciones_borradas_mes += 1
        usuario.cotizaciones_borradas_totales += 1
        usuario.fecha_ultima_cot = datetime.today()
        usuario.save()
    if request.method == 'POST' and request.POST.get("eliminar_gig"):
        cambiado = True
        orden_a_eliminar = models.OrdenesGigantografia.objects.get(num_solicitud_ot=request.POST.get("orden_gig"))

        orden_a_eliminar.delete()
        usuario = models.Usuarios.objects.get(username=request.user)
        fecha_ultima = usuario.fecha_ultima_ot.month
        hoy = datetime.now().month
        print(fecha_ultima,hoy)
        if fecha_ultima != hoy:
            usuario.ordenes_borradas_mes = 0
        usuario.ordenes_borradas_mes += 1
        usuario.ordenes_borradas_totales += 1
        usuario.fecha_ultima_ot = datetime.today()
        usuario.save()
    else:
        cambiado = False

    return render(request, 'eliminar_solicitud.html',{"gig_eliminar":gig_eliminar,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,
        "ordenes_eliminar":ordenes_eliminar,"cotizaciones_eliminar":cotizaciones_eliminar,'cambiado': cambiado,"usuarios_existentes":usuarios_existentes,"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"cotizaciones_existentes":cotizaciones_existentes
    })


@login_required
def change_password(request):
    cambiado = False
    usuarios_existentes = models.Usuarios.objects.all()
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':
        cambiado = True
        u = models.Usuarios.objects.get(username=request.POST.get("usuario"))
        u.set_password(request.POST.get("contraseña"))
        u.save()
    else:
        cambiado = False

    return render(request, 'cambio_contraseña.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,
        'cambiado': cambiado,"usuarios_existentes":usuarios_existentes,"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"cotizaciones_existentes":cotizaciones_existentes
    })


@login_required
def change_password(request):
    cambiado = False
    usuarios_existentes = models.Usuarios.objects.all()
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':
        cambiado = True
        u = models.Usuarios.objects.get(username=request.POST.get("usuario"))
        u.set_password(request.POST.get("contraseña"))
        u.save()
    else:
        cambiado = False

    return render(request, 'cambio_contraseña.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,
    'cambiado': cambiado,"usuarios_existentes":usuarios_existentes,"ordenes_existentes":ordenes_existentes,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"cotizaciones_existentes":cotizaciones_existentes
    })

@login_required
def ordenes_sin_fecha(request):
    buscar = False
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    hoy = datetime.today().date()
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        else:
            ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        print(ordenes_por_fecha)
        return render(request, "ordenes_sin_fecha.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        else:
            ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
        return render(request, "ordenes_sin_fecha.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_fecha") == "ESTABLECER FECHA DE ENTREGA":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)

        orden.fecha_entrega_ot = request.POST.get("fecha")





        orden.save()
        return HttpResponseRedirect(reverse('ordenes_sin_fecha'))


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")
        ordenes_por_fecha = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_a_ver)
        hoy = datetime.today().date()
        return render(request, "ordenes_sin_fecha.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})


@login_required
def confirmacion_material(request):
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    buscar = False
    if request.method == "POST" and request.POST.get("confirmado"):
        orden_a_confirmar = models.OrdenesSolicitadas.objects.get(num_solicitud_ot=request.POST.get("orden_a_confirmar"))
        orden_a_confirmar.material_confirmado = True
        orden_a_confirmar.save()

    return render(request, "ordenes_confirmar_material.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"buscar":buscar,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_proceso":ordenes_proceso,"ordenes_por_confirmar":ordenes_por_confirmar,"cotizaciones_existentes":cotizaciones_existentes,})


@login_required
def ordenes_en_proceso(request):
    buscar = False
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    hoy = datetime.today().date()
    print(hoy)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).order_by("fecha_entrega_ot")
        else:
            ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        print(ordenes_proceso)
        return render(request, "ordenes_en_proceso.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(vendedor_ot=request.user).order_by("fecha_entrega_ot")
        else:
            ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        return render(request, "ordenes_en_proceso.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_terminado") == "ORDEN TERMINADA":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)

        orden.estado_ot = "Orden terminada"
        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso'))

    elif request.method == "POST" and request.POST.get("boton_cerrar") == "CERRAR OT":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)

        orden.estado_ot = "Cerrada"
        orden.fecha_entregada = date.today()




        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso'))
    elif request.method == "POST" and request.POST.get("boton_parcial") == "ENTREGA PARCIAL":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)

        if orden.estado_ot == "Orden aperturada" or orden.estado_ot == "Orden terminada":
            orden.estado_ot = "Parcial entregado: " + str(request.POST.get("cantidad_entregada"))
            orden.fecha_entregada = date.today()
        else:
            cantidad_parcial = orden.estado_ot.split()
            cantidad_calculada = int(cantidad_parcial[-1]) + int(request.POST.get("cantidad_entregada"))
            orden.estado_ot = "Parcial entregado: " + str(cantidad_calculada)
            orden.fecha_entregada = date.today()







        orden.save()
        return HttpResponseRedirect(reverse('ordenes_en_proceso'))

        #return render(request,"ordenes_en_proceso.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"orden_completada":orden_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")

        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_a_ver)
        return render(request, "ordenes_en_proceso.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"hoy":hoy,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})



@login_required
def ordenes_aperturadas(request):
    ver = False
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    clientes_creados = models.Clientes_ot.objects.all().order_by("nombre_razon_social")
    trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
    vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
    tipo_busqueda = ""
    if request.method == "GET" and request.user.categoria == "VEN":
        ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("tipo_busqueda"):

        desde = request.POST.get("desde")
        hasta = request.POST.get("hasta")
        print("AQUIIII",desde,hasta)
        if request.user.categoria == "VEN":
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "Trabajo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.all().filter(tipo_trabajo_ot=request.POST.get("busqueda")).filter(vendedor_ot=request.user).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("busqueda"))
                ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")



            elif request.POST.get("tipo_busqueda") == "Solicitud":
                ordenes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=request.POST.get("busqueda")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Orden":
                ordenes = OrdenesSolicitadas.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("busqueda")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Orden"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                ordenes = OrdenesSolicitadas.objects.all().filter(trabajo_ot__istartswith=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        else:
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "trabajo_ot"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.all().filter(tipo_trabajo_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("busqueda"))
                ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")


            elif request.POST.get("tipo_busqueda") == "Vendedor":
                tipo_busqueda = "Vendedor"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.all().filter(vendedor_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Cotizador":
                tipo_busqueda = "Cotizador"
                busqueda = request.POST.get("busqueda")
                ordenes = OrdenesSolicitadas.objects.all().filter(cotizador_ot=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
            elif request.POST.get("tipo_busqueda") == "Solicitud":
                ordenes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=request.POST.get("busqueda")).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Orden":
                ordenes = OrdenesSolicitadas.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("busqueda")).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Orden"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                ordenes = OrdenesSolicitadas.objects.all().filter(trabajo_ot__istartswith=request.POST.get("busqueda")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        paginator = Paginator(ordenes,10)
        if request.POST.get("boton") == "siguiente":
            page = request.POST.get("pagina_siguiente")
        else:
            page = request.POST.get("pagina_anterior")
        ordenes_completadas = paginator.get_page(page)

        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"busqueda":busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "siguiente":
        if request.user.categoria == "VEN":
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.POST.get("pagina_siguiente")
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "anterior":
        if request.user.categoria == "VEN":
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.POST.get("pagina_anterior")
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes = OrdenesSolicitadas.objects.all().filter(vendedor_ot=request.user).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        print("aqui")
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        print("prueba")

        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("buscar") == "BUSCAR":
        if request.user.categoria == "VEN":
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cl"))
                    ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    ordenes = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    ordenes = OrdenesSolicitadas.objects.all().filter(tipo_trabajo_ot=request.POST.get("tr")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")
                    ordenes = OrdenesSolicitadas.objects.all().filter(vendedor_ot=request.POST.get("ven")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    ordenes = OrdenesSolicitadas.objects.all().filter(cotizador_ot=request.POST.get("cot")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Solicitud":
                    ordenes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=request.POST.get("parametro")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Orden":
                    ordenes = OrdenesSolicitadas.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("parametro")).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Orden"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesSolicitadas.objects.all().filter(trabajo_ot__istartswith=request.POST.get("parametro")).filter(fecha_completada_ot__range=[desde,hasta]).filter(vendedor_ot=request.user).order_by("-fecha_solicitada_ot")
                print("si")
                clientes_creados = models.Clientes_ot.objects.all().order_by("nombre_razon_social")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(ordenes,10)
                page = request.GET.get('page')
                ordenes_completadas = paginator.get_page(page)
                return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})

        else:
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cl"))
                    ordenes = b.client_ot.all().filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    ordenes = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    ordenes = OrdenesSolicitadas.objects.all().filter(tipo_trabajo_ot=request.POST.get("tr")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")

                    ordenes = OrdenesSolicitadas.objects.all().filter(vendedor_ot=request.POST.get("ven")).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    ordenes = OrdenesSolicitadas.objects.all().filter(cotizador_ot=request.POST.get("cot")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Solicitud":
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=request.POST.get("parametro")).order_by("-fecha_solicitada_ot")
                elif request.POST.get("seleccion") == "Orden":
                    tipo_busqueda = "Orden"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesSolicitadas.objects.all().filter(num_ot_relacionada__istartswith=request.POST.get("parametro")).order_by("-fecha_solicitada_ot")

                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    ordenes = OrdenesSolicitadas.objects.all().filter(trabajo_ot__istartswith=request.POST.get("parametro")).filter(fecha_completada_ot__range=[desde,hasta]).order_by("-fecha_solicitada_ot")
                print("si")
                clientes_creados = models.Clientes.objects.all().order_by("nombre")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(ordenes,10)
                page = request.GET.get('page')
                ordenes_completadas = paginator.get_page(page)
                return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ordenes_completadas":ordenes_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})
    if request.method == "POST" and request.POST.get("ver") == "ver orden":
        ver = True

        orden_buscada = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=request.POST.get("cot_ver"))

        return render(request, "ordenes_aperturadas.html",{"ordenes_existentes":ordenes_existentes,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_buscada":orden_buscada,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})

        return render(request, "ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_buscada":orden_buscada,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})



    if request.method == "POST" and request.POST.get("regresar") == "REGRESAR":
        ver = False
        if request.user.categoria == "VEN":
            ordenes = OrdenesSolicitadas.objects.all().filter(vendedor_ot=request.user).exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        else:
            ordenes = OrdenesSolicitadas.objects.all().exclude(cotizador_ot__exact="").order_by("-fecha_solicitada_ot")
        paginator = Paginator(ordenes,10)
        page = request.GET.get('page')
        ordenes_completadas = paginator.get_page(page)
        return render(request,"ordenes_aperturadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_completadas":ordenes_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR":
        cot = request.POST.get("cot_reutilizar")
        request.session['cot'] = cot

        return HttpResponseRedirect(reverse('solicitud'))

        #return render(request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ver_cinta":ver_cinta,"orden":orden,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"orden_encontrada":orden_encontrada,"ordenes_existentes":ordenes_existentes} )


@login_required
def ordenes_por_aperturar(request):
    buscar = False
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="").filter(vendedor_ot=request.user)
        else:
            ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        print(ordenes_existentes)
        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="").filter(vendedor_ot=request.user)
        else:
            ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"ordenes_existentes":ordenes_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_completar") == "COMPLETAR":
        buscar=False
        numero_1 = request.POST.get("numero1")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)
        cot = CotizacionesSolicitadas.objects.get(solicitud_ot=numero_1)
        orden.fecha_completada_ot = datetime.now()
        orden.cotizador_ot = str(request.user)
        orden.num_ot_relacionada = request.POST.get("orden_papyrus")
        orden.estado_ot = "Orden aperturada"
        orden.permiso_borrar = False
        cot.num_ot_relacionada = request.POST.get("orden_papyrus")
        cot.permiso_borrar = False

        orden.save()
        cot.save()
        return HttpResponseRedirect(reverse('ordenes_por_aperturar'))
    elif request.method == "POST" and request.POST.get("asignar") == "ASIGNAR":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)
        orden.procesado_por_ot = str(request.user)
        orden.save()

        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes":ordenes_existentes})
    elif request.method == "POST" and request.POST.get("borrar") == "HABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)
        orden.permiso_borrar = True
        orden.save()


        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes":ordenes_existentes})


        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes":ordenes_existentes})




    elif request.method == "POST" and request.POST.get("borrar") == "DESHABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_1)
        ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        orden = OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_1)
        orden.permiso_borrar = False
        orden.save()

        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_1, "ordenes_existentes":ordenes_existentes})


        #return render(request,"ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"orden_completada":orden_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})


    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")
        ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        orden_existentes = OrdenesSolicitadas.objects.all().filter(num_solicitud_ot=numero_a_ver)
        return render(request, "ordenes_por_aperturar.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes,"orden_existentes":orden_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "ordenes_existentes":ordenes_existentes})



def solicitud_ot(request):
    solicitado = False
    tipo_trabajo = ""
    busqueda = False
    aprobada = False
    materiales = ""
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    numero_solicitud = ""
    tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    materiales = models.Materiales.objects.all().order_by("material")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")



    if request.method == "GET" and 'tipo_trabajo' in request.session:
        if request.session['tipo_trabajo'] != "":
            ver_cinta = ""



            orden_utilizar = OrdenesSolicitadas()
            cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=request.session["numero"])


            nombre_cliente = models.Clientes.objects.get(nombre=cotizacion.nombre_cliente)
            try:
                cliente_ot = nombre_cliente.client_razon_social.get(nombre=cotizacion.nombre_cliente)
            except models.Clientes_ot.DoesNotExist:
                 return HttpResponseRedirect(reverse("error01"))


            orden_utilizar.nombre_cliente_ot= cliente_ot
            orden_utilizar.trabajo_ot = request.session['trabajo']
            orden_utilizar.cantidad_ot = request.session['cantidad']

            orden_utilizar.vendedor_ot = request.user
            orden_utilizar.tipo_trabajo_ot = request.session['tipo_trabajo']
            orden_utilizar.material_ot = request.session['material']
            orden_utilizar.descripcion_material_ot = request.session['descripcion_material']
            orden_utilizar.medida_alto_ot = request.session['medida_alto']
            orden_utilizar.medida_ancho_ot = request.session['medida_ancho']

            orden_utilizar.impresion_tiro_ot = request.session['impresion_tiro']

            orden_utilizar.impresion_retiro_ot = request.session['impresion_retiro']
            orden_utilizar.uv_ot = request.session['uv']
            orden_utilizar.laminado_ot = request.session['laminado']
            orden_utilizar.troquelado_ot = request.session['troquelado']

            orden_utilizar.material2_ot = request.session['material2']
            orden_utilizar.descripcion_material2_ot = request.session['descripcion_material2']
            orden_utilizar.medida_alto_2_ot = request.session['medida_alto_2']
            orden_utilizar.medida_ancho_2_ot = request.session['medida_ancho_2']
            orden_utilizar.impresion_tiro2_ot = request.session['impresion_tiro2']
            orden_utilizar.impresion_retiro2_ot = request.session['impresion_retiro2']
            orden_utilizar.uv2_ot = request.session['uv2']
            orden_utilizar.laminado2_ot = request.session['laminado2']
            orden_utilizar.troquelado2_ot = request.session['troquelado2']

            orden_utilizar.material3_ot = request.session['material3']
            orden_utilizar.descripcion_material3_ot = request.session['descripcion_material3']
            orden_utilizar.medida_alto_3_ot = request.session['medida_alto_3']
            orden_utilizar.medida_ancho_3_ot = request.session['medida_ancho_3']
            orden_utilizar.impresion_tiro3_ot = request.session['impresion_tiro3']
            orden_utilizar.impresion_retiro3_ot = request.session['impresion_retiro3']
            orden_utilizar.uv3_ot = request.session['uv3']
            orden_utilizar.laminado3_ot = request.session['laminado3']
            orden_utilizar.troquelado3_ot = request.session['troquelado3']


            orden_utilizar.material4_ot = request.session['material4']
            orden_utilizar.descripcion_material4_ot = request.session['descripcion_material4']
            orden_utilizar.medida_alto_4_ot = request.session['medida_alto_4']
            orden_utilizar.medida_ancho_4_ot = request.session['medida_ancho_4']
            orden_utilizar.impresion_tiro4_ot = request.session['impresion_tiro4']
            orden_utilizar.impresion_retiro4_ot = request.session['impresion_retiro4']
            orden_utilizar.uv4_ot = request.session['uv4']
            orden_utilizar.laminado4_ot = request.session['laminado4']
            orden_utilizar.troquelado4_ot = request.session['troquelado4']


            orden_utilizar.material5_ot = request.session['material5']
            orden_utilizar.descripcion_material5_ot = request.session['descripcion_material5']
            orden_utilizar.medida_alto_5_ot = request.session['medida_alto_5']
            orden_utilizar.medida_ancho_5_ot = request.session['medida_ancho_5']
            orden_utilizar.impresion_tiro5_ot = request.session['impresion_tiro5']
            orden_utilizar.impresion_retiro5_ot = request.session['impresion_retiro5']
            orden_utilizar.uv5_ot = request.session['uv5']
            orden_utilizar.laminado5_ot = request.session['laminado5']
            orden_utilizar.troquelado5_ot = request.session['troquelado5']


            orden_utilizar.detalles_ot = request.session['detalles']

            if orden_utilizar.detalles_ot != "":
                detalle = orden_utilizar.detalles_ot.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto2 = " ".join(texto)
                            orden_utilizar.detalles_ot = texto2
                except:

                    pass



            orden_encontrada = orden_utilizar
            data = {"nombre_cliente_ot":orden_encontrada.nombre_cliente_ot,"trabajo_ot":orden_encontrada.trabajo_ot,"cantidad_ot":orden_encontrada.cantidad_ot}
            orden = Solicitud_ot_aprobacion(user=request.user,data=data)
            orden.fields["nombre_cliente_ot"].disabled = True
            orden.fields["nombre_cliente_ot"].initial = orden_encontrada.nombre_cliente_ot
            orden.fields["trabajo_ot"].disabled = True
            orden.fields["trabajo_ot"].initial = orden_encontrada.trabajo_ot
            orden.fields["cantidad_ot"].disabled = True
            orden.fields["cantidad_ot"].initial = orden_encontrada.cantidad_ot
            print(orden_encontrada.impresion_tiro_ot)

            busqueda = True
            tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
            materiales = models.Materiales.objects.all().order_by("material")
            aprobada = True
            request.session["tipo_de_trabajo"] = request.session["tipo_trabajo"]
            request.session["tipo_trabajo"] = ""

            return render(request, "solicitud_ot.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion":cotizacion,"ver_cinta":ver_cinta,"aprobada":aprobada,"orden":orden,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"orden_encontrada":orden_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )


    if request.method == "POST" and request.POST.get("Buscar"):
        ot = request.POST.get("ot_reutilizar")
        ver_cinta = ""
        aprobada = False
        try:
            orden_encontrada = models.OrdenesSolicitadas.objects.get(num_solicitud_ot = ot)
            cliente_nombre = str(orden_encontrada.nombre_cliente_ot)
            print(cliente_nombre)
            cliente_nombre = cliente_nombre.split()
            del cliente_nombre[0]
            cliente_nombre = " ".join(cliente_nombre)
            cliente_encontrado = models.Clientes_ot.objects.get(nombre_razon_social=cliente_nombre)
            if cliente_encontrado.desactivado == True:
                return HttpResponseRedirect(reverse("error01"))
            print("AQUI",orden_encontrada)
            if orden_encontrada.detalles_ot != "" and orden_encontrada.detalles_ot != None:
                detalle = orden_encontrada.detalles_ot.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto2 = " ".join(texto)
                            orden_encontrada.detalles_ot = texto2
                except:

                    pass



            if orden_encontrada.numero_cotizacion_ot != "" and orden_encontrada.numero_cotizacion_ot != None and orden_encontrada.detalles_ot != None:
                detalle = orden_encontrada.detalles_ot.split("\n")
                texto_cot_papyrus = detalle[-1].split()
                if len(texto_cot_papyrus) != 0:
                    texto_cot_papyrus = texto_cot_papyrus[-1].split()
                    print(texto_cot_papyrus[0][0])
                    if texto_cot_papyrus[0][0] == "#":
                        print("si")
                        detalles_finales = orden_encontrada.detalles_ot.split("\n")
                        print(detalles_finales)
                        referencia = detalles_finales[-1].split()
                        print(referencia)
                        referencia[-1] = "#" + str(orden_encontrada.numero_cotizacion_ot)
                        print(referencia)
                        referencia = " ".join(referencia)
                        print(referencia)
                        detalles_finales[-1] = referencia
                        orden_encontrada.detalles_ot = " ".join(detalles_finales)
                else:
                    orden_encontrada.detalles_ot += "\n" + "Referencia COT PAPYRUS #" + str(orden_encontrada.numero_cotizacion_ot)
            data = {"nombre_cliente_ot":orden_encontrada.nombre_cliente_ot,"trabajo_ot":orden_encontrada.trabajo_ot,"cantidad_ot":orden_encontrada.cantidad_ot}
            orden = Solicitud_ot(user=request.user,data=data)

        except OrdenesSolicitadas.DoesNotExist:
            orden_encontrada = "NO HAY"
            orden = Solicitud_ot(request.user)
        busqueda = True
        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")


        return render(request, "solicitud_ot.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ver_cinta":ver_cinta,"orden":orden,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"orden_encontrada":orden_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )

    if request.method == 'POST' and request.POST.get("solicitud"):



        #data = {"nombre_cliente_ot":request.session["nombre_cliente"],"trabajo_ot":request.session["trabajo"],"cantidad_ot":request.session["cantidad"]}
        orden = Solicitud_ot(user=request.user)

        print("orden valida")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=request.session["numero"])

        stock = orden.save(commit=False)
        print(request.session["trabajo"])
        stock.vendedor_ot = request.user
        nombre_cliente = models.Clientes.objects.get(nombre=cotizacion.nombre_cliente)
        cliente_ot = nombre_cliente.client_razon_social.get(nombre=cotizacion.nombre_cliente)
        stock.nombre_cliente_ot = cliente_ot
        stock.cantidad_ot = request.session["cantidad"]
        stock.trabajo_ot = request.session["trabajo"]

        stock.direccion_entrega = request.POST.get("direccion")
        stock.persona_recibe = request.POST.get("persona")
        stock.forma_empaque = request.POST.get("empaque")

        stock.tipo_impresion = request.POST.get("tipo_impresion")
        if request.POST.get("arte") == "on":
            stock.arte = True
        if request.POST.get("dummie") == "on":
            stock.dummie = True
        if request.POST.get("machote") == "on":
            stock.machote = True
        if request.POST.get("prueba_de_color") == "on":
            stock.prueba_de_color = True
        if request.POST.get("muestra_real") == "on":
            stock.muestra_real = True

        stock.tipo_trabajo_ot = request.session['tipo_de_trabajo']
        stock.material_ot = request.session['material']
        stock.descripcion_material_ot = request.session['descripcion_material']
        stock.medida_alto_ot = request.session['medida_alto']
        stock.medida_ancho_ot = request.session['medida_ancho']
        if request.POST.get("nombre_pantonest1"):
            stock.impresion_tiro_ot = request.session['impresion_tiro'] + " Colores: " +  request.POST.get("nombre_pantonest1")
        else:
            stock.impresion_tiro_ot = request.session['impresion_tiro']
        if request.POST.get("nombre_pantonesr1"):
            stock.impresion_retiro_ot = request.session['impresion_retiro'] + " Colores: " +  request.POST.get("nombre_pantonesr1")
        else:
            stock.impresion_retiro_ot = request.session['impresion_retiro']
        stock.uv_ot = request.session['uv']
        stock.laminado_ot = request.session['laminado']
        stock.troquelado_ot = request.session['troquelado']

        stock.material2_ot = request.session['material2']
        stock.descripcion_material2_ot = request.session['descripcion_material2']
        stock.medida_alto_2_ot = request.session['medida_alto_2']
        stock.medida_ancho_2_ot = request.session['medida_ancho_2']
        if request.POST.get("nombre_pantonest2"):
            stock.impresion_tiro2_ot = request.session['impresion_tiro2'] + " Colores: " +  request.POST.get("nombre_pantonest2")
        else:
            stock.impresion_tiro2_ot = request.session['impresion_tiro2']
        if request.POST.get("nombre_pantonesr2"):
            stock.impresion_retiro2_ot = request.session['impresion_retiro2'] + " Colores: " +  request.POST.get("nombre_pantonesr2")
        else:
            stock.impresion_retiro2_ot = request.session['impresion_retiro2']
        stock.uv2_ot = request.session['uv2']
        stock.laminado2_ot = request.session['laminado2']
        stock.troquelado2_ot = request.session['troquelado2']

        stock.material3_ot = request.session['material3']
        stock.descripcion_material3_ot = request.session['descripcion_material3']
        stock.medida_alto_3_ot = request.session['medida_alto_3']
        stock.medida_ancho_3_ot = request.session['medida_ancho_3']
        if request.POST.get("nombre_pantonest3"):
            stock.impresion_tiro3_ot = request.session['impresion_tiro3'] + " Colores: " +  request.POST.get("nombre_pantonest3")
        else:
            stock.impresion_tiro3_ot = request.session['impresion_tiro3']
        if request.POST.get("nombre_pantonesr3"):
            stock.impresion_retiro3_ot = request.session['impresion_retiro3'] + " Colores: " +  request.POST.get("nombre_pantonesr3")
        else:
            stock.impresion_retiro3_ot = request.session['impresion_retiro3']
        stock.uv3_ot = request.session['uv3']
        stock.laminado3_ot = request.session['laminado3']
        stock.troquelado3_ot = request.session['troquelado3']


        stock.material4_ot = request.session['material4']
        stock.descripcion_material4_ot = request.session['descripcion_material4']
        stock.medida_alto_4_ot = request.session['medida_alto_4']
        stock.medida_ancho_4_ot = request.session['medida_ancho_4']
        if request.POST.get("nombre_pantonest4"):
            stock.impresion_tiro4_ot = request.session['impresion_tiro4'] + " Colores: " +  request.POST.get("nombre_pantonest4")
        else:
            stock.impresion_tiro4_ot = request.session['impresion_tiro4']
        if request.POST.get("nombre_pantonesr4"):
            stock.impresion_retiro4_ot = request.session['impresion_retiro4'] + " Colores: " +  request.POST.get("nombre_pantonesr4")
        else:
            stock.impresion_retiro4_ot = request.session['impresion_retiro4']
        stock.uv4_ot = request.session['uv4']
        stock.laminado4_ot = request.session['laminado4']
        stock.troquelado4_ot = request.session['troquelado4']


        stock.material5_ot = request.session['material5']
        stock.descripcion_material5_ot = request.session['descripcion_material5']
        stock.medida_alto_5_ot = request.session['medida_alto_5']
        stock.medida_ancho_5_ot = request.session['medida_ancho_5']
        if request.POST.get("nombre_pantonest5"):
            stock.impresion_tiro5_ot = request.session['impresion_tiro5'] + " Colores: " +  request.POST.get("nombre_pantonest5")
        else:
            stock.impresion_tiro5_ot = request.session['impresion_tiro5']
        if request.POST.get("nombre_pantonesr5"):
            stock.impresion_retiro5_ot = request.session['impresion_retiro5'] + " Colores: " +  request.POST.get("nombre_pantonesr5")
        else:
            stock.impresion_retiro5_ot = request.session['impresion_retiro5']
        stock.uv5_ot = request.session['uv5']
        stock.laminado5_ot = request.session['laminado5']
        stock.troquelado5_ot = request.session['troquelado5']


        stock.detalles_ot = ""
        if request.POST.get("cantidad_cintas") != None:

            stock.detalles_ot = str(request.POST.get("cantidad_cintas")) + " pedazos de " + str(request.POST.get("tipo_cinta"))
            stock.detalles_ot += " de " + str(request.POST.get("cm_cintas")) + " cms" + "\n"
        if request.POST.get("adicional"):

            stock.detalles_ot += request.POST.get("adicional") + request.POST.get("adicional_texto")+ "\n"



        stock.detalles_ot += request.POST.get("detalles")

        if request.POST.get("solicitud"):
            stock.numero_cotizacion_ot = request.POST.get("cotizacion")

        stock.save()
        numero_solicitud = models.OrdenesSolicitadas.objects.all().last()
        cotizacion.solicitud_ot = numero_solicitud.num_solicitud_ot
        cotizacion.save()
        request.session["tipo_trabajo"] = ""
        solicitado = True
        busqueda = False
        ot_modelo = models.TipoDeTrabajo.objects.all()

        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")

        return render(request, 'solicitud_ot.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})


    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR ULTIMA ORDEN":
        cot = request.POST.get("cot_reutilizar_ult")
        ver_cinta = ""
        try:
            orden_encontrada = models.OrdenesSolicitadas.objects.get(num_solicitud_ot = cot)
            print("AQUIII",orden_encontrada)
            if orden_encontrada.detalles_ot != "" and orden_encontrada.detalles_ot != None:
                detalle = orden_encontrada.detalles_ot.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto = " ".join(texto)
                            orden_encontrada.detalles_ot = texto
                except:

                    pass



            if orden_encontrada.numero_cotizacion_ot != "" and orden_encontrada.numero_cotizacion_ot != None:

                orden_encontrada.detalles_ot += "\n" + "Referencia COT PAPYRUS #" + str(orden_encontrada.numero_cotizacion_ot)
            data = {"nombre_cliente_ot":orden_encontrada.nombre_cliente_ot,"trabajo_ot":orden_encontrada.trabajo_ot,"cantidad_ot":orden_encontrada.cantidad_ot}
            orden = Solicitud_ot(user=request.user,data=data)

        except OrdenesSolicitadas.DoesNotExist:
            orden_encontrada = "NO HAY"
            print("HOLA")
            orden = Solicitud_ot(request.user)
        busqueda = True
        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")



        return render(request, 'solicitud_ot.html',{"orden":orden,"orden_encontrada":orden_encontrada,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})

    if request.method == 'POST':

        orden = Solicitud_ot(user=request.user,data=request.POST)
        if orden.is_valid():
            print("orden valida")
            stock = orden.save(commit=False)
            stock.vendedor_ot = request.user

            stock.direccion_entrega = request.POST.get("direccion")
            stock.persona_recibe = request.POST.get("persona")
            stock.forma_empaque = request.POST.get("empaque")

            stock.tipo_trabajo_ot = request.POST.get("opciones")
            stock.material_ot = request.POST.get("material1")
            stock.descripcion_material_ot = request.POST.get("descripcion")
            stock.medida_alto_ot = request.POST.get("alto1")
            stock.medida_ancho_ot = request.POST.get("ancho1")
            stock.impresion_tiro_ot = str(request.POST.get("num_pantonest1")) + " " + str(request.POST.get("impresiont1"))
            if request.POST.get("impresionr1") == None:
                stock.impresion_retiro_ot = "Sin impresion"
            else:
                stock.impresion_retiro_ot = str(request.POST.get("num_pantonesr1")) + " " + str(request.POST.get("impresionr1"))

            stock.uv_ot = request.POST.get("uv1")
            stock.laminado_ot = request.POST.get("laminado1")
            if request.POST.get("troquel1"):
                stock.troquelado_ot = str(request.POST.get("troquel1")) + " " +  str(request.POST.get("troquel_existente1"))
            else:
                stock.troquelado_ot = str(request.POST.get("troqueladh1")) + " " + str(request.POST.get("troquel_existente1"))

            stock.material2_ot = request.POST.get("material2")
            stock.descripcion_material2_ot = request.POST.get("descripcion2")
            stock.medida_alto_2_ot = request.POST.get("alto2")
            stock.medida_ancho_2_ot = request.POST.get("ancho2")
            stock.impresion_tiro2_ot = str(request.POST.get("num_pantonest2")) + " " + str(request.POST.get("impresiont2"))
            if request.POST.get("impresionr2") == None:
                stock.impresion_retiro2_ot = "Sin impresion"
            else:
                stock.impresion_retiro2_ot = str(request.POST.get("num_pantonesr2")) + " " + str(request.POST.get("impresionr2"))
            stock.uv2_ot = request.POST.get("uv2")
            stock.laminado2_ot = request.POST.get("laminado2")
            if request.POST.get("troquel2"):
                stock.troquelado2_ot = str(request.POST.get("troquel2")) + " " +  str(request.POST.get("troquel_existente2"))
            else:
                stock.troquelado2_ot = str(request.POST.get("troqueladh2")) + " " + str(request.POST.get("troquel_existente2"))
            stock.material3_ot = request.POST.get("material3")
            stock.descripcion_material3_ot = request.POST.get("descripcion3")
            stock.medida_alto_3_ot = request.POST.get("alto3")
            stock.medida_ancho_3_ot = request.POST.get("ancho3")
            stock.impresion_tiro3_ot = str(request.POST.get("num_pantonest3")) + " " + str(request.POST.get("impresiont3"))
            if request.POST.get("impresionr3") == None:
                stock.impresion_retiro3_ot = "Sin impresion"
            else:
                stock.impresion_retiro3_ot = str(request.POST.get("num_pantonesr3")) + " " + str(request.POST.get("impresionr3"))
            stock.uv3_ot = request.POST.get("uv3")
            stock.laminado3_ot = request.POST.get("laminado3")
            if request.POST.get("troquel3"):
                stock.troquelado3_ot = str(request.POST.get("troquel3")) + " " +  str(request.POST.get("troquel_existente3"))
            else:
                stock.troquelado3_ot = str(request.POST.get("troqueladh3")) + " " + str(request.POST.get("troquel_existente3"))

            stock.material4_ot = request.POST.get("material4")
            stock.descripcion_material4_ot = request.POST.get("descripcion4")
            stock.medida_alto_4_ot = request.POST.get("alto4")
            stock.medida_ancho_4_ot = request.POST.get("ancho4")
            stock.impresion_tiro4_ot = str(request.POST.get("num_pantonest4")) + " " + str(request.POST.get("impresiont4"))
            if request.POST.get("impresionr4") == None:
                stock.impresion_retiro4_ot = "Sin impresion"
            else:
                stock.impresion_retiro4_ot = str(request.POST.get("num_pantonesr4")) + " " + str(request.POST.get("impresionr4"))
            stock.uv4_ot = request.POST.get("uv4")
            stock.laminado4_ot = request.POST.get("laminado4")
            if request.POST.get("troquel4"):
                stock.troquelado4_ot = str(request.POST.get("troquel4")) + " " +  str(request.POST.get("troquel_existente4"))
            else:
                stock.troquelado4_ot = str(request.POST.get("troqueladh4")) + " " + str(request.POST.get("troquel_existente4"))

            stock.material5_ot = request.POST.get("material5")
            stock.descripcion_material5_ot = request.POST.get("descripcion5")
            stock.medida_alto_5_ot = request.POST.get("alto5")
            stock.medida_ancho_5_ot = request.POST.get("ancho5")
            stock.impresion_tiro5_ot = str(request.POST.get("num_pantonest5")) + " " + str(request.POST.get("impresiont5"))
            if request.POST.get("impresionr5") == None:
                stock.impresion_retiro5_ot = "Sin impresion"
            else:
                stock.impresion_retiro5_ot = str(request.POST.get("num_pantonesr5")) + " " + str(request.POST.get("impresionr5"))
            stock.uv5_ot = request.POST.get("uv5")
            stock.laminado5_ot = request.POST.get("laminado5")
            if request.POST.get("troquel5"):
                stock.troquelado5_ot = str(request.POST.get("troquel5")) + " " +  str(request.POST.get("troquel_existente5"))
            else:
                stock.troquelado5_ot = str(request.POST.get("troqueladh5")) + " " + str(request.POST.get("troquel_existente5"))


            stock.detalles_ot = ""
            if request.POST.get("cantidad_cintas") != None:

                stock.detalles_ot = str(request.POST.get("cantidad_cintas")) + " pedazos de " + str(request.POST.get("tipo_cinta"))
                stock.detalles_ot += " de " + str(request.POST.get("cm_cintas")) + " cms" + "\n"
            if request.POST.get("adicional"):

                stock.detalles_ot += request.POST.get("adicional") + request.POST.get("adicional_texto")+ "\n"



            stock.detalles_ot += request.POST.get("detalles")

            if request.POST.get("solicitud"):
                stock.numero_cotizacion_ot = request.POST.get("cotizacion")

            stock.save()
            solicitado = True
            busqueda = False
            ot_modelo = models.TipoDeTrabajo.objects.all()
            numero_solicitud = models.OrdenesSolicitadas.objects.all().last()
            tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
            materiales = models.Materiales.objects.all().order_by("material")
            # do something.

            nombre_con_codigo = models.OrdenesSolicitadas.objects.get(num_solicitud_ot=numero_solicitud.num_solicitud_ot)
            cotizacion = Solicitud_cot(user=request.user)

            nombre_sin_codigo = str(nombre_con_codigo.nombre_cliente_ot).split()
            del nombre_sin_codigo[0]
            nombre_sin_codigo = " ".join(nombre_sin_codigo)
            stock2 = cotizacion.save(commit=False)
            stock2.cantidad = stock.cantidad_ot
            stock2.trabajo = stock.trabajo_ot
            print(nombre_sin_codigo)
            nombre_cliente = models.Clientes_ot.objects.get(nombre_razon_social=nombre_sin_codigo)
            #cliente_ot = nombre_cliente.client_razon_social.get(nombre=cotizacion.nombre_cliente)


            stock2.nombre_cliente = nombre_cliente.nombre
            stock2.vendedor = request.user
            stock2.tipo_trabajo = request.POST.get("opciones")
            stock2.material = request.POST.get("material1")
            stock2.descripcion_material = request.POST.get("descripcion")
            stock2.medida_alto = request.POST.get("alto1")
            stock2.medida_ancho = request.POST.get("ancho1")
            stock2.impresion_tiro = str(request.POST.get("num_pantonest1")) + " " + str(request.POST.get("impresiont1"))
            stock2.impresion_retiro = str(request.POST.get("num_pantonesr1")) + " " + str(request.POST.get("impresionr1"))

            stock2.solicitud_ot = numero_solicitud.num_solicitud_ot

            stock2.uv = request.POST.get("uv1")
            stock2.laminado = request.POST.get("laminado1")
            if request.POST.get("troquel1"):
                stock2.troquelado = str(request.POST.get("troquel1")) + " " +  str(request.POST.get("troquel_existente1"))
            else:
                stock2.troquelado = str(request.POST.get("troqueladh1")) + " " + str(request.POST.get("troquel_existente1"))

            stock2.material2 = request.POST.get("material2")
            stock2.descripcion_material2 = request.POST.get("descripcion2")
            stock2.medida_alto_2 = request.POST.get("alto2")
            stock2.medida_ancho_2 = request.POST.get("ancho2")
            stock2.impresion_tiro2 = str(request.POST.get("num_pantonest2")) + " " + str(request.POST.get("impresiont2"))
            stock2.impresion_retiro2 = str(request.POST.get("num_pantonesr2")) + " " + str(request.POST.get("impresionr2"))
            stock2.uv2 = request.POST.get("uv2")
            stock2.laminado2 = request.POST.get("laminado2")
            if request.POST.get("troquel2"):
                stock2.troquelado2 = str(request.POST.get("troquel2")) + " " +  str(request.POST.get("troquel_existente2"))
            else:
                stock2.troquelado2 = str(request.POST.get("troqueladh2")) + " " + str(request.POST.get("troquel_existente2"))
            stock2.material3 = request.POST.get("material3")
            stock2.descripcion_material3 = request.POST.get("descripcion3")
            stock2.medida_alto_3 = request.POST.get("alto3")
            stock2.medida_ancho_3 = request.POST.get("ancho3")
            stock2.impresion_tiro3 = str(request.POST.get("num_pantonest3")) + " " + str(request.POST.get("impresiont3"))
            stock2.impresion_retiro3 = str(request.POST.get("num_pantonesr3")) + " " + str(request.POST.get("impresionr3"))
            stock2.uv3 = request.POST.get("uv3")
            stock2.laminado3 = request.POST.get("laminado3")
            if request.POST.get("troquel3"):
                stock2.troquelado3 = str(request.POST.get("troquel3")) + " " +  str(request.POST.get("troquel_existente3"))
            else:
                stock2.troquelado3 = str(request.POST.get("troqueladh3")) + " " + str(request.POST.get("troquel_existente3"))

            stock2.material4 = request.POST.get("material4")
            stock2.descripcion_material4 = request.POST.get("descripcion4")
            stock2.medida_alto_4 = request.POST.get("alto4")
            stock2.medida_ancho_4 = request.POST.get("ancho4")
            stock2.impresion_tiro4 = str(request.POST.get("num_pantonest4")) + " " + str(request.POST.get("impresiont4"))
            stock2.impresion_retiro4 = str(request.POST.get("num_pantonesr4")) + " " + str(request.POST.get("impresionr4"))
            stock2.uv4 = request.POST.get("uv4")
            stock2.laminado4 = request.POST.get("laminado4")
            if request.POST.get("troquel4"):
                stock2.troquelado4 = str(request.POST.get("troquel4")) + " " +  str(request.POST.get("troquel_existente4"))
            else:
                stock2.troquelado4 = str(request.POST.get("troqueladh4")) + " " + str(request.POST.get("troquel_existente4"))

            stock2.material5 = request.POST.get("material5")
            stock2.descripcion_material5 = request.POST.get("descripcion5")
            stock2.medida_alto_5 = request.POST.get("alto5")
            stock2.medida_ancho_5 = request.POST.get("ancho5")
            stock2.impresion_tiro5 = str(request.POST.get("num_pantonest5")) + " " + str(request.POST.get("impresiont5"))
            stock2.impresion_retiro5 = str(request.POST.get("num_pantonesr5")) + " " + str(request.POST.get("impresionr5"))
            stock2.uv5 = request.POST.get("uv5")
            stock2.laminado5 = request.POST.get("laminado5")
            if request.POST.get("troquel5"):
                stock2.troquelado5 = str(request.POST.get("troquel5")) + " " +  str(request.POST.get("troquel_existente5"))
            else:
                stock2.troquelado5 = str(request.POST.get("troqueladh5")) + " " + str(request.POST.get("troquel_existente5"))


            stock2.detalles = ""
            if request.POST.get("cantidad_cintas") != None:

                stock2.detalles = str(request.POST.get("cantidad_cintas")) + " pedazos de " + str(request.POST.get("tipo_cinta"))
                stock2.detalles += " de " + str(request.POST.get("cm_cintas")) + " cms" + "\n"
            if request.POST.get("adicional"):

                stock2.detalles += request.POST.get("adicional") + request.POST.get("adicional_texto")+ "\n"



            stock2.detalles += request.POST.get("detalles")
            if "imagen" in request.FILES:
                stock2.imagen = request.FILES["imagen"]


            stock2.save()
            num_solicitud_cot = models.CotizacionesSolicitadas.objects.all().last()
            stock = models.OrdenesSolicitadas.objects.all().last()
            stock.solicitud_cot = num_solicitud_cot.num_solicitud
            stock.save()

        return render(request, 'solicitud_ot.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})


    else:
        orden = Solicitud_ot(user=request.user)
        solicitado = False


        busqueda = False
        ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")

        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")

        return render(request, 'solicitud_ot.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"busqueda":busqueda,"cotizaciones_existentes":cotizaciones_existentes,"numero_solicitud":numero_solicitud,"orden":orden,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "ordenes_existentes":ordenes_existentes})



# Create your views here.
def home(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':

        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'home.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes})


def error01(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    request.session['tipo_trabajo'] = ""
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")


    return render(request, "error01.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes})


def contactenos(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':

        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "contactanos.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes})

def quienes_somos(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':

        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "compañia.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes})

def servicios(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':

        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "servicios.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_existentes":ordenes_existentes,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizaciones_existentes":cotizaciones_existentes})

def solicitud(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    return render( request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes})

def creacion_usuario(request):
    registered = False
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == 'POST':

        usuario = Crear_usuario(data=request.POST)
        if usuario.is_valid():
            usuario_creado = usuario.save()
            usuario_creado.set_password(usuario_creado.password)
            usuario_creado.save()

            registered = True
            # do something.
    else:
        usuario = Crear_usuario()
    return render(request, 'registro.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_existentes":ordenes_existentes,'usuario': usuario, "registered":registered,"cotizaciones_existentes":cotizaciones_existentes})

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'home.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,})

@login_required
def solicitud_cot(request):
    solicitado = False
    tipo_trabajo = ""
    busqueda = False
    materiales = ""
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    numero_solicitud = ""
    tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    materiales = models.Materiales.objects.all().order_by("material")
    if request.method == "GET":
        print("yap")
        try:
            if request.session['cot'] != "":
                cot = request.session['cot']
                request.session['cot'] = ""
                ver_cinta = ""
                print("yep")
                try:
                    cotizacion_encontrada = models.CotizacionesSolicitadas.objects.get(num_solicitud = cot)
                    print("AQUI",cotizacion_encontrada)
                    if cotizacion_encontrada.detalles != "":
                        detalle = cotizacion_encontrada.detalles.split("\n")
                        ver_cinta = detalle[0].split()

                        detalle[0] = detalle[0].split()

                        try:
                            if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                                texto = detalle[0][8:] + detalle[1:]
                                print(texto)
                                if len(texto) != 0:
                                    texto = " ".join(texto)
                                    cotizacion_encontrada.detalles = texto
                        except:

                            pass



                    if cotizacion_encontrada.numero_cotizacion != "":
                        detalle = cotizacion_encontrada.detalles.split("\n")
                        texto_cot_papyrus = detalle[-1].split()
                        if len(texto_cot_papyrus) != 0:
                            texto_cot_papyrus = texto_cot_papyrus[-1].split()
                            print(texto_cot_papyrus[0][0])
                            if texto_cot_papyrus[0][0] == "#":
                                print("si")
                                detalles_finales = cotizacion_encontrada.detalles.split("\n")
                                print(detalles_finales)
                                referencia = detalles_finales[-1].split()
                                print(referencia)
                                referencia[-1] = "#" + str(cotizacion_encontrada.numero_cotizacion)
                                print(referencia)
                                referencia = " ".join(referencia)
                                print(referencia)
                                detalles_finales[-1] = referencia
                                cotizacion_encontrada.detalles = " ".join(detalles_finales)

                            else:
                                cotizacion_encontrada.detalles += "\n" + "Referencia COT PAPYRUS #" + str(cotizacion_encontrada.numero_cotizacion)
                        else:
                                cotizacion_encontrada.detalles += "\n" + "Referencia COT PAPYRUS #" + str(cotizacion_encontrada.numero_cotizacion)
                    else:
                            pass

                    data = {"nombre_cliente":cotizacion_encontrada.nombre_cliente,"trabajo":cotizacion_encontrada.trabajo,"cantidad":cotizacion_encontrada.cantidad}
                    cotizacion = Solicitud_cot(user=request.user,data=data)

                except CotizacionesSolicitadas.DoesNotExist:
                    cotizacion_encontrada = "NO HAY"
                    cotizacion = Solicitud_cot(request.user)
                busqueda = True
                tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                materiales = models.Materiales.objects.all().order_by("material")


                return render(request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ver_cinta":ver_cinta,"cotizacion":cotizacion,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"cotizacion_encontrada":cotizacion_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )
        except:
            pass
    if request.method == "POST" and request.POST.get("Buscar"):
        cot = request.POST.get("cot_reutilizar")
        ver_cinta = ""
        try:
            cotizacion_encontrada = models.CotizacionesSolicitadas.objects.get(num_solicitud = cot)
            cliente_encontrado = models.Clientes.objects.get(nombre=cotizacion_encontrada.nombre_cliente)
            if cliente_encontrado.desactivado == True:
                return HttpResponseRedirect(reverse("error01"))
            print("AQUI",cotizacion_encontrada)
            if cotizacion_encontrada.detalles != "":
                detalle = cotizacion_encontrada.detalles.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto2 = " ".join(texto)
                            cotizacion_encontrada.detalles = texto2
                except:

                    pass



            if cotizacion_encontrada.numero_cotizacion != "":
                        detalle = cotizacion_encontrada.detalles.split("\n")
                        texto_cot_papyrus = detalle[-1].split()
                        if len(texto_cot_papyrus) != 0:
                            texto_cot_papyrus = texto_cot_papyrus[-1].split()
                            print(texto_cot_papyrus[0][0])
                            if texto_cot_papyrus[0][0] == "#":
                                print("si")
                                detalles_finales = cotizacion_encontrada.detalles.split("\n")
                                print(detalles_finales)
                                referencia = detalles_finales[-1].split()
                                print(referencia)
                                referencia[-1] = "#" + str(cotizacion_encontrada.numero_cotizacion)
                                print(referencia)
                                referencia = " ".join(referencia)
                                print(referencia)
                                detalles_finales[-1] = referencia
                                cotizacion_encontrada.detalles = " ".join(detalles_finales)

                            else:
                                if cotizacion_encontrada.numero_cotizacion != "":
                                    cotizacion_encontrada.detalles += "\n" + "Referencia COT PAPYRUS #" + str(cotizacion_encontrada.numero_cotizacion)
                        else:
                            if cotizacion_encontrada.numero_cotizacion != "":
                                cotizacion_encontrada.detalles += "\n" + "Referencia COT PAPYRUS #" + str(cotizacion_encontrada.numero_cotizacion)
            data = {"nombre_cliente":cotizacion_encontrada.nombre_cliente,"trabajo":cotizacion_encontrada.trabajo,"cantidad":cotizacion_encontrada.cantidad}
            cotizacion = Solicitud_cot(user=request.user,data=data)

        except CotizacionesSolicitadas.DoesNotExist:
            cotizacion_encontrada = "NO HAY"
            cotizacion = Solicitud_cot(request.user)
        busqueda = True
        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")


        return render(request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ver_cinta":ver_cinta,"cotizacion":cotizacion,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"cotizacion_encontrada":cotizacion_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )

    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR ULTIMA COTIZACION":
        cot = request.POST.get("cot_reutilizar_ult")
        ver_cinta = ""
        try:
            cotizacion_encontrada = models.CotizacionesSolicitadas.objects.get(num_solicitud = cot)
            print("AQUI",cotizacion_encontrada)
            if cotizacion_encontrada.detalles != "" and cotizacion_encontrada.detalles != None:
                detalle = cotizacion_encontrada.detalles.split("\n")
                ver_cinta = detalle[0].split()

                detalle[0] = detalle[0].split()

                try:
                    if detalle[0][4] == "roja" or detalle[0][4] == "blanca":
                        texto = detalle[0][8:] + detalle[1:]
                        print(texto)
                        if len(texto) != 0:
                            texto = " ".join(texto)
                            cotizacion_encontrada.detalles = texto
                except:

                    pass



            if cotizacion_encontrada.numero_cotizacion != "" and cotizacion_encontrada.numero_cotizacion != None:

                cotizacion_encontrada.detalles += "\n" + "Referencia COT PAPYRUS #" + str(cotizacion_encontrada.numero_cotizacion)
            data = {"nombre_cliente":cotizacion_encontrada.nombre_cliente,"trabajo":cotizacion_encontrada.trabajo,"cantidad":cotizacion_encontrada.cantidad}
            cotizacion = Solicitud_cot(user=request.user,data=data)

        except CotizacionesSolicitadas.DoesNotExist:
            cotizacion_encontrada = "NO HAY"
            cotizacion = Solicitud_cot(request.user)
        busqueda = True
        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")


        return render(request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"ver_cinta":ver_cinta,"cotizacion":cotizacion,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"cotizacion_encontrada":cotizacion_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )


    elif request.method == 'POST':

        cotizacion = Solicitud_cot(user=request.user,data=request.POST)
        if cotizacion.is_valid():
            stock = cotizacion.save(commit=False)
            stock.vendedor = request.user
            stock.tipo_trabajo = request.POST.get("opciones")
            stock.material = request.POST.get("material1")
            stock.descripcion_material = request.POST.get("descripcion")
            stock.medida_alto = request.POST.get("alto1")
            stock.medida_ancho = request.POST.get("ancho1")
            stock.impresion_tiro = request.POST.get("num_pantonest1") + " " + request.POST.get("impresiont1")

            if request.POST.get("impresionr1"):
                stock.impresion_retiro = str(request.POST.get("num_pantonesr1")) + " " + str(request.POST.get("impresionr1"))

            else:
                stock.impresion_retiro = "Sin impresion"
            stock.uv = request.POST.get("uv1")
            stock.laminado = request.POST.get("laminado1")
            if request.POST.get("troquel1"):
                stock.troquelado = str(request.POST.get("troquel1")) + " " +  str(request.POST.get("troquel_existente1"))
            else:
                stock.troquelado = str(request.POST.get("troqueladh1")) + " " + str(request.POST.get("troquel_existente1"))

            stock.material2 = request.POST.get("material2")
            stock.descripcion_material2 = request.POST.get("descripcion2")
            stock.medida_alto_2 = request.POST.get("alto2")
            stock.medida_ancho_2 = request.POST.get("ancho2")
            stock.impresion_tiro2 = str(request.POST.get("num_pantonest2")) + " " + str(request.POST.get("impresiont2"))
            if request.POST.get("impresionr1"):
                stock.impresion_retiro2 = str(request.POST.get("num_pantonesr2")) + " " + str(request.POST.get("impresionr2"))

            else:
                stock.impresion_retiro2 = "Sin impresion"
            stock.uv2 = request.POST.get("uv2")
            stock.laminado2 = request.POST.get("laminado2")
            if request.POST.get("troquel2"):
                stock.troquelado2 = str(request.POST.get("troquel2")) + " " +  str(request.POST.get("troquel_existente2"))
            else:
                stock.troquelado2 = str(request.POST.get("troqueladh2")) + " " + str(request.POST.get("troquel_existente2"))
            stock.material3 = request.POST.get("material3")
            stock.descripcion_material3 = request.POST.get("descripcion3")
            stock.medida_alto_3 = request.POST.get("alto3")
            stock.medida_ancho_3 = request.POST.get("ancho3")
            stock.impresion_tiro3 = str(request.POST.get("num_pantonest3")) + " " + str(request.POST.get("impresiont3"))
            if request.POST.get("impresionr3"):
                stock.impresion_retiro3 = str(request.POST.get("num_pantonesr3")) + " " + str(request.POST.get("impresionr3"))

            else:
                stock.impresion_retiro3 = "Sin impresion"
            stock.uv3 = request.POST.get("uv3")
            stock.laminado3 = request.POST.get("laminado3")
            if request.POST.get("troquel3"):
                stock.troquelado3 = str(request.POST.get("troquel3")) + " " +  str(request.POST.get("troquel_existente3"))
            else:
                stock.troquelado3 = str(request.POST.get("troqueladh3")) + " " + str(request.POST.get("troquel_existente3"))

            stock.material4 = request.POST.get("material4")
            stock.descripcion_material4 = request.POST.get("descripcion4")
            stock.medida_alto_4 = request.POST.get("alto4")
            stock.medida_ancho_4 = request.POST.get("ancho4")
            stock.impresion_tiro4 = str(request.POST.get("num_pantonest4")) + " " + str(request.POST.get("impresiont4"))
            if request.POST.get("impresionr4"):
                stock.impresion_retiro4 = str(request.POST.get("num_pantonesr4")) + " " + str(request.POST.get("impresionr4"))

            else:
                stock.impresion_retiro4 = "Sin impresion"
            stock.uv4 = request.POST.get("uv4")
            stock.laminado4 = request.POST.get("laminado4")
            if request.POST.get("troquel4"):
                stock.troquelado4 = str(request.POST.get("troquel4")) + " " +  str(request.POST.get("troquel_existente4"))
            else:
                stock.troquelado4 = str(request.POST.get("troqueladh4")) + " " + str(request.POST.get("troquel_existente4"))

            stock.material5 = request.POST.get("material5")
            stock.descripcion_material5 = request.POST.get("descripcion5")
            stock.medida_alto_5 = request.POST.get("alto5")
            stock.medida_ancho_5 = request.POST.get("ancho5")
            stock.impresion_tiro5 = str(request.POST.get("num_pantonest5")) + " " + str(request.POST.get("impresiont5"))
            if request.POST.get("impresionr1"):
                stock.impresion_retiro5 = str(request.POST.get("num_pantonesr5")) + " " + str(request.POST.get("impresionr5"))

            else:
                stock.impresion_retiro5 = "Sin impresion"
            stock.uv5 = request.POST.get("uv5")
            stock.laminado5 = request.POST.get("laminado5")
            if request.POST.get("troquel5"):
                stock.troquelado5 = str(request.POST.get("troquel5")) + " " +  str(request.POST.get("troquel_existente5"))
            else:
                stock.troquelado5 = str(request.POST.get("troqueladh5")) + " " + str(request.POST.get("troquel_existente5"))


            stock.detalles = ""
            if request.POST.get("cantidad_cintas") != None:

                stock.detalles = str(request.POST.get("cantidad_cintas")) + " pedazos de " + str(request.POST.get("tipo_cinta"))
                stock.detalles += " de " + str(request.POST.get("cm_cintas")) + " cms" + "\n"
            if request.POST.get("adicional"):

                stock.detalles += request.POST.get("adicional") + request.POST.get("adicional_texto")+ "\n"



            stock.detalles += request.POST.get("detalles")
            if "imagen" in request.FILES:
                stock.imagen = request.FILES["imagen"]
            stock.save()
            solicitado = True
            busqueda = False
            cot_modelo = models.TipoDeTrabajo.objects.all()
            numero_solicitud = models.CotizacionesSolicitadas.objects.all().last()
            tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
            materiales = models.Materiales.objects.all().order_by("material")
            # do something.
    else:
        cotizacion = Solicitud_cot(user=request.user)
        solicitado = False
        busqueda = False
        ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")

        tipo_trabajo = models.TipoDeTrabajo.objects.all().order_by("trabajo")
        materiales = models.Materiales.objects.all().order_by("material")
    return render(request, 'solicitud.html',{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"numero_solicitud":numero_solicitud,"cotizacion":cotizacion,"solicitado":solicitado,"materiales":materiales, "tipo_trabajo":tipo_trabajo, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def solicitudes_existentes(request):
    buscar = False
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    if request.method == "GET":
        if request.user.categoria == "VEN":
            cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="").filter(vendedor=request.user)
        else:
            cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        print(cotizaciones_existentes)
        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"buscar":buscar})
    elif request.method == "POST" and request.POST.get("boton_regresar") == "REGRESAR":
        buscar=False
        if request.user.categoria == "VEN":
            cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="").filter(vendedor=request.user)
        else:
            cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"buscar":buscar})

    elif request.method == "POST" and request.POST.get("boton_completar") == "COMPLETAR":
        buscar=False
        numero_1 = request.POST.get("numero1")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=numero_1)

        cotizacion.fecha_completada = datetime.now()
        cotizacion.cotizador = str(request.user)
        cotizacion.numero_cotizacion = request.POST.get("cotizacion_papyrus")
        cotizacion.permiso_borrar = False

        try:
            orden = models.OrdenesSolicitadas.objects.get(solicitud_cot=cotizacion.num_solicitud)
            orden.numero_cotizacion_ot = request.POST.get("cotizacion_papyrus")
            orden.permiso_borrar = False
            orden.save()
        except models.OrdenesSolicitadas.DoesNotExist:
            pass
        cotizacion.save()



        return HttpResponseRedirect(reverse('solicitudes_existentes'))
    elif request.method == "POST" and request.POST.get("asignar") == "ASIGNAR":
        buscar = True
        numero_1 = request.POST.get("numero1")
        cotizacion_existentes = CotizacionesSolicitadas.objects.all().filter(num_solicitud=numero_1)
        cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=numero_1)
        cotizacion.procesado_por = str(request.user)
        cotizacion.save()

        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_1, "cotizaciones_existentes":cotizaciones_existentes})
    elif request.method == "POST" and request.POST.get("borrar") == "DESHABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        cotizacion_existentes = CotizacionesSolicitadas.objects.all().filter(num_solicitud=numero_1)
        cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=numero_1)
        cotizacion.permiso_borrar = False
        cotizacion.save()


        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_1, "cotizaciones_existentes":cotizaciones_existentes})
    elif request.method == "POST" and request.POST.get("borrar") == "HABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        cotizacion_existentes = CotizacionesSolicitadas.objects.all().filter(num_solicitud=numero_1)
        cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=numero_1)
        cotizacion.permiso_borrar = True
        cotizacion.save()

        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_1, "cotizaciones_existentes":cotizaciones_existentes})


        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_1, "cotizaciones_existentes":cotizaciones_existentes})
    elif request.method == "POST" and request.POST.get("borrar") == "HABILITAR ELIMINACION":
        buscar = True
        numero_1 = request.POST.get("numero1")
        cotizacion_existentes = CotizacionesSolicitadas.objects.all().filter(num_solicitud=numero_1)
        cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        cotizacion = CotizacionesSolicitadas.objects.get(num_solicitud=numero_1)
        cotizacion.permiso_borrar = True
        cotizacion.save()

        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_1, "cotizaciones_existentes":cotizaciones_existentes})











        #return render(request,"solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizacion_completada":cotizacion_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})


        #return render(request,"solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"cotizacion_completada":cotizacion_completada,"buscar":buscar,"numero_a_ver":numero_a_ver})
    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR":
        cot = request.POST.get("cot_ver")
        request.session['cot'] = cot
        print(cot)
        return HttpResponseRedirect(reverse('solicitud'))

    elif request.method == "POST":
        buscar = True
        numero_a_ver = request.POST.get("numero")
        cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
        cotizacion_existentes = CotizacionesSolicitadas.objects.all().filter(num_solicitud=numero_a_ver)
        return render(request, "solicitudes_existentes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_existentes":cotizacion_existentes, "buscar":buscar, "numero_a_ver":numero_a_ver, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def cotizaciones_completadas(request):
    ver = False
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    clientes_creados = models.Clientes.objects.all().order_by("nombre")
    trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
    vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
    tipo_busqueda = ""
    if request.method == "GET" and request.user.categoria == "VEN":
        cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")
        paginator = Paginator(cotizaciones,10)
        page = request.GET.get('page')
        cotizaciones_completadas = paginator.get_page(page)
        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("tipo_busqueda"):

        desde = request.POST.get("desde")
        hasta = request.POST.get("hasta")
        print("AQUIIII",desde,hasta)
        if request.user.categoria == "VEN":
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "Trabajo"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(tipo_trabajo=request.POST.get("busqueda")).filter(vendedor=request.user).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes.objects.get(nombre=request.POST.get("busqueda"))
                cotizaciones = b.client.all().filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")



            elif request.POST.get("tipo_busqueda") == "Solicitud":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(num_solicitud=request.POST.get("busqueda")).filter(vendedor=request.user).order_by("-fecha_solicitada")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Cotizacion":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(numero_cotizacion__istartswith=request.POST.get("busqueda")).filter(vendedor=request.user).order_by("-fecha_solicitada")
                tipo_busqueda = "Cotizacion"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(trabajo__istartswith=request.POST.get("busqueda")).filter(fecha_completada__range=[desde,hasta]).filter(vendedor=request.user).order_by("-fecha_solicitada")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        else:
            if request.POST.get("tipo_busqueda") == "Trabajo":
                tipo_busqueda = "Trabajo"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(tipo_trabajo=request.POST.get("busqueda")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
            elif request.POST.get("tipo_busqueda") == "Cliente":
                print(request.POST.get("cl"))
                tipo_busqueda = "Cliente"
                busqueda = request.POST.get("busqueda")
                b = models.Clientes.objects.get(nombre=request.POST.get("busqueda"))
                cotizaciones = b.client.all().filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").order_by("-fecha_solicitada")


            elif request.POST.get("tipo_busqueda") == "Todo":
                print("TODO")
                tipo_busqueda = "Todo"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").order_by("-fecha_solicitada")


            elif request.POST.get("tipo_busqueda") == "Vendedor":
                tipo_busqueda = "Vendedor"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(vendedor=request.POST.get("busqueda")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
            elif request.POST.get("tipo_busqueda") == "Cotizador":
                tipo_busqueda = "Cotizador"
                busqueda = request.POST.get("busqueda")
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(cotizador=request.POST.get("busqueda")).filter(fecha_completada__range=[desde,hasta]).order_by("-fecha_solicitada")
            elif request.POST.get("tipo_busqueda") == "Solicitud":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(num_solicitud=request.POST.get("busqueda")).order_by("-fecha_solicitada")
                tipo_busqueda = "Solicitud"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Cotizacion":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(numero_cotizacion__istartswith=request.POST.get("busqueda")).order_by("-fecha_solicitada")
                tipo_busqueda = "Cotizacion"
                busqueda = request.POST.get("busqueda")
            elif request.POST.get("tipo_busqueda") == "Promocion":
                cotizaciones = CotizacionesSolicitadas.objects.all().filter(trabajo__istartswith=request.POST.get("busqueda")).filter(fecha_completada__range=[desde,hasta]).order_by("-fecha_solicitada")
                tipo_busqueda = "Promocion"
                busqueda = request.POST.get("busqueda")
        paginator = Paginator(cotizaciones,10)
        if request.POST.get("boton") == "siguiente":
            page = request.POST.get("pagina_siguiente")
        else:
            page = request.POST.get("pagina_anterior")
        cotizaciones_completadas = paginator.get_page(page)

        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"busqueda":busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "siguiente":
        if request.user.categoria == "VEN":
            cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")
        else:
            cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").order_by("-fecha_solicitada")
        paginator = Paginator(cotizaciones,10)
        page = request.POST.get("pagina_siguiente")
        cotizaciones_completadas = paginator.get_page(page)
        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "POST" and request.POST.get("boton") == "anterior":
        if request.user.categoria == "VEN":
            cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")
        else:
            cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").order_by("-fecha_solicitada")
        paginator = Paginator(cotizaciones,10)
        page = request.POST.get("pagina_anterior")
        cotizaciones_completadas = paginator.get_page(page)
        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    elif request.method == "GET":
        cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="").order_by("-fecha_solicitada")
        paginator = Paginator(cotizaciones,10)
        print("aqui")
        page = request.GET.get('page')
        cotizaciones_completadas = paginator.get_page(page)
        print("prueba")

        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("buscar") == "BUSCAR":
        if request.user.categoria == "VEN":
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes.objects.get(nombre=request.POST.get("cl"))
                    cotizaciones = b.client.all().filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    cotizaciones = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(tipo_trabajo=request.POST.get("tr")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").filter(vendedor=request.user).order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(vendedor=request.POST.get("ven")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(cotizador=request.POST.get("cot")).filter(fecha_completada__range=[desde,hasta]).order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Solicitud":
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(num_solicitud=request.POST.get("parametro")).filter(vendedor=request.user).order_by("-fecha_solicitada")
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Cotizacion":
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(numero_cotizacion__istartswith=request.POST.get("parametro")).filter(vendedor=request.user).order_by("-fecha_solicitada")
                    tipo_busqueda = "Cotizacion"
                    busqueda = request.POST.get("parametro")
                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(trabajo__istartswith=request.POST.get("parametro")).filter(fecha_completada__range=[desde,hasta]).filter(vendedor=request.user).order_by("-fecha_solicitada")
                print("si")
                clientes_creados = models.Clientes.objects.all().order_by("nombre")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(cotizaciones,10)
                page = request.GET.get('page')
                cotizaciones_completadas = paginator.get_page(page)
                return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})

        else:
            try:
                ver = False
                desde = request.POST.get("desde")
                hasta = request.POST.get("hasta")
                print("DESDE",desde)
                print("HASTA",hasta)

                print("SIRVE " + request.POST.get("parametro"))
                if request.POST.get("seleccion") == "Cliente":
                    print(request.POST.get("cl"))
                    b = models.Clientes.objects.get(nombre=request.POST.get("cl"))
                    cotizaciones = b.client.all().filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
                    tipo_busqueda = "Cliente"
                    busqueda = request.POST.get("cl")

                elif request.POST.get("seleccion") == "Todo":
                    print("TODO")
                    tipo_busqueda = "Todo"
                    busqueda = ""
                    cotizaciones = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador__exact="").order_by("-fecha_solicitada")

                elif request.POST.get("seleccion") == "Trabajo":
                    tipo_busqueda = "Trabajo"
                    busqueda = request.POST.get("tr")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(tipo_trabajo=request.POST.get("tr")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Vendedor":
                    tipo_busqueda = "Vendedor"
                    busqueda = request.POST.get("ven")

                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(vendedor=request.POST.get("ven")).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador__exact="").order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Cotizador":
                    tipo_busqueda = "Cotizador"
                    busqueda = request.POST.get("cot")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(cotizador=request.POST.get("cot")).filter(fecha_completada__range=[desde,hasta]).order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Solicitud":
                    tipo_busqueda = "Solicitud"
                    busqueda = request.POST.get("parametro")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(num_solicitud=request.POST.get("parametro")).order_by("-fecha_solicitada")
                elif request.POST.get("seleccion") == "Cotizacion":
                    tipo_busqueda = "Cotizacion"
                    busqueda = request.POST.get("parametro")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(numero_cotizacion__istartswith=request.POST.get("parametro")).order_by("-fecha_solicitada")

                elif request.POST.get("seleccion") == "Promocion":
                    tipo_busqueda = "Promocion"
                    busqueda = request.POST.get("parametro")
                    cotizaciones = CotizacionesSolicitadas.objects.all().filter(trabajo=request.POST.get("parametro")).filter(fecha_completada__range=[desde,hasta]).order_by("-fecha_solicitada")
                print("si")
                clientes_creados = models.Clientes.objects.all().order_by("nombre")
                trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
                cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
                vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
                paginator = Paginator(cotizaciones,10)
                page = request.GET.get('page')
                cotizaciones_completadas = paginator.get_page(page)
                return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"busqueda":busqueda,"desde":desde,"hasta":hasta,"tipo_busqueda":tipo_busqueda,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
            except:

                return render(request, "cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_existentes":cotizaciones_existentes,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores})
    if request.method == "POST" and request.POST.get("ver") == "ver cotizacion":
        ver = True

        cotizacion_buscada = CotizacionesSolicitadas.objects.all().filter(num_solicitud=request.POST.get("cot_ver"))
        return render(request, "cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizacion_buscada":cotizacion_buscada,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"ver":ver,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("solicitar") == "Solicitar OT":

        cotizacion_aperturar = CotizacionesSolicitadas.objects.get(num_solicitud=request.POST.get("cot_ver"))


        request.session["cantidad"] = cotizacion_aperturar.cantidad
        request.session["trabajo"] = cotizacion_aperturar.trabajo
        request.session["numero"] = cotizacion_aperturar.num_solicitud

        request.session["tipo_trabajo"] = cotizacion_aperturar.tipo_trabajo
        request.session["material"]= cotizacion_aperturar.material
        request.session["descripcion_material"] = cotizacion_aperturar.descripcion_material
        request.session["medida_alto"]= cotizacion_aperturar.medida_alto
        request.session["medida_ancho"]= cotizacion_aperturar.medida_ancho
        request.session["impresion_tiro"] = cotizacion_aperturar.impresion_tiro
        request.session["impresion_retiro"] = cotizacion_aperturar.impresion_retiro
        request.session["uv"] = cotizacion_aperturar.uv
        request.session["laminado"] = cotizacion_aperturar.laminado
        request.session["troquelado"] = cotizacion_aperturar.troquelado



        request.session["material2"]= cotizacion_aperturar.material2
        request.session["descripcion_material2"] = cotizacion_aperturar.descripcion_material2
        request.session["medida_alto_2"]= cotizacion_aperturar.medida_alto_2
        request.session["medida_ancho_2"]= cotizacion_aperturar.medida_ancho_2
        request.session["impresion_tiro2"] = cotizacion_aperturar.impresion_tiro2
        request.session["impresion_retiro2"] = cotizacion_aperturar.impresion_retiro2
        request.session["uv2"] = cotizacion_aperturar.uv2
        request.session["laminado2"] = cotizacion_aperturar.laminado2
        request.session["troquelado2"] = cotizacion_aperturar.troquelado2


        request.session["material3"]= cotizacion_aperturar.material3
        request.session["descripcion_material3"] = cotizacion_aperturar.descripcion_material3
        request.session["medida_alto_3"]= cotizacion_aperturar.medida_alto_3
        request.session["medida_ancho_3"]= cotizacion_aperturar.medida_ancho_3
        request.session["impresion_tiro3"] = cotizacion_aperturar.impresion_tiro3
        request.session["impresion_retiro3"] = cotizacion_aperturar.impresion_retiro3
        request.session["uv3"] = cotizacion_aperturar.uv3
        request.session["laminado3"] = cotizacion_aperturar.laminado3
        request.session["troquelado3"] = cotizacion_aperturar.troquelado3


        request.session["material4"]= cotizacion_aperturar.material4
        request.session["descripcion_material4"] = cotizacion_aperturar.descripcion_material4
        request.session["medida_alto_4"]= cotizacion_aperturar.medida_alto_4
        request.session["medida_ancho_4"]= cotizacion_aperturar.medida_ancho_4
        request.session["impresion_tiro4"] = cotizacion_aperturar.impresion_tiro4
        request.session["impresion_retiro4"] = cotizacion_aperturar.impresion_retiro4
        request.session["uv4"] = cotizacion_aperturar.uv4
        request.session["laminado4"] = cotizacion_aperturar.laminado4
        request.session["troquelado4"] = cotizacion_aperturar.troquelado4


        request.session["material5"]= cotizacion_aperturar.material5
        request.session["descripcion_material5"] = cotizacion_aperturar.descripcion_material5
        request.session["medida_alto_5"]= cotizacion_aperturar.medida_alto_5
        request.session["medida_ancho_5"]= cotizacion_aperturar.medida_ancho_5
        request.session["impresion_tiro5"] = cotizacion_aperturar.impresion_tiro5
        request.session["impresion_retiro5"] = cotizacion_aperturar.impresion_retiro5
        request.session["uv5"] = cotizacion_aperturar.uv5
        request.session["laminado5"] = cotizacion_aperturar.laminado5
        request.session["troquelado5"] = cotizacion_aperturar.troquelado5


        request.session["detalles"] = cotizacion_aperturar.detalles
        #request.session['cot_aperturar'] = cotizacion_aperturar

        return HttpResponseRedirect(reverse('solicitud_ot'))


    if request.method == "POST" and request.POST.get("regresar") == "REGRESAR":
        ver = False
        cotizaciones = CotizacionesSolicitadas.objects.all().exclude(cotizador__exact="")
        paginator = Paginator(cotizaciones,10)
        page = request.GET.get('page')
        cotizaciones_completadas = paginator.get_page(page)
        return render(request,"cotizaciones_completadas.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cotizaciones_completadas":cotizaciones_completadas,"ver":ver,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores, "cotizaciones_existentes":cotizaciones_existentes})

    if request.method == "POST" and request.POST.get("reutilizar") == "REUTILIZAR":
        cot = request.POST.get("cot_ver")
        request.session['cot'] = cot

        return HttpResponseRedirect(reverse('solicitud'))

        #return render(request, "solicitud.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ver_cinta":ver_cinta,"cotizacion":cotizacion,"tipo_trabajo":tipo_trabajo,"materiales":materiales,"busqueda":busqueda,"cotizacion_encontrada":cotizacion_encontrada,"cotizaciones_existentes":cotizaciones_existentes} )

@login_required
def creacion_material(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        material = Materiales(data=request.POST)
        if material.is_valid():
            creacion = material.save(commit=False)
            creacion.usuario = request.user
            creacion.material = creacion.material.title()
            creacion.save()
            creado = True
    else:
            material = Materiales()
    return render(request, "materiales.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"material":material, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def creacion_trabajo(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        trabajo = TipoDeTrabajo(data=request.POST)
        if trabajo.is_valid():
            creacion = trabajo.save(commit=False)
            creacion.trabajo = creacion.trabajo.title()
            creacion.usuario = request.user
            creacion.save()
            creado = True
    else:
            trabajo = TipoDeTrabajo()
    return render(request, "tipos_trabajo.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"trabajo":trabajo, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def creacion_cliente(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        cliente = Clientes(data=request.POST)
        if cliente.is_valid():
            creacion= cliente.save(commit=False)
            creacion.nombre = creacion.nombre.title()
            creacion.usuario = request.user
            creacion.save()


            creado = True
    else:
            cliente = Clientes()
    return render(request, "clientes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cliente":cliente, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def creacion_cliente_ot(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    creado = False
    if request.method == "POST" and request.POST.get("crear") == "CREAR":
        cliente = Clientes_ot(user=request.user,data=request.POST)
        print("aqui",models.Clientes.objects.get(id=request.POST.get("nombre")))

        cliente_cot = models.Clientes.objects.get(nombre=models.Clientes.objects.get(id=request.POST.get("nombre")))
        cliente_cot.nombre_razon_social = request.POST.get("nombre_razon_social").title()
        #b = models.Clientes.objects.get(nombre=request.POST.get("cl"))
        #ordenes = b.client.all().filter(fecha_completada__range=[str(desde),str(hasta)]).exclude(cotizador_ot__exact="").filter(vendedor_ot=request.user)

        if cliente.is_valid():
            creacion= cliente.save(commit=False)
            creacion.nombre_razon_social = creacion.nombre_razon_social.title()
            creacion.usuario = request.user
            creacion.vendedor_asociado = cliente_cot.vendedor_asociado
            creacion.save()
            cliente_cot.save()


            creado = True
    else:
            cliente = Clientes_ot(user=request.user)
    return render(request, "clientes_ot.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"cliente":cliente, "creado":creado, "cotizaciones_existentes":cotizaciones_existentes})

@login_required
def bloqueo_clientes(request):
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    clientes = models.Clientes_ot.objects.all().filter(desactivado=False)
    clientes_bloq = models.Clientes_ot.objects.all().filter(desactivado=True)
    bloqueado = False
    texto = ""
    if request.method == "POST" and request.POST.get("bloqueo") == "Bloquear":

        cliente_a_bloquear = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cliente"))
        cliente_a_bloquear.desactivado = True
        cliente_a_bloquear.save()
        texto = "BLOQUEADO"
        bloqueado = True


    if request.method == "POST" and request.POST.get("desbloqueo") == "Desbloquear":

        cliente_a_bloquear = models.Clientes_ot.objects.get(nombre_razon_social=request.POST.get("cliente_bloq"))
        cliente_a_bloquear.desactivado = False
        cliente_a_bloquear.save()
        texto = "DESBLOQUEADO"
        bloqueado = True



    return render(request, "bloqueo_clientes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"ordenes_por_confirmar":ordenes_por_confirmar,"texto":texto,"clientes_bloq":clientes_bloq,"clientes":clientes,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes, "bloqueado":bloqueado, "cotizaciones_existentes":cotizaciones_existentes})


@login_required
def reportes(request):
    ordenes_por_confirmar = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").exclude(material_confirmado=True)
    ordenes_existentes_gig = OrdenesGigantografia.objects.all().filter(cotizador_ot__exact="")
    ordenes_por_fecha_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    ordenes_proceso_gig = OrdenesGigantografia.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    cotizaciones_existentes = CotizacionesSolicitadas.objects.all().filter(cotizador__exact="")
    clientes_creados = models.Clientes.objects.all().order_by("nombre")
    trabajos_creados = models.TipoDeTrabajo.objects.all().order_by("trabajo")
    cotizadores = models.Usuarios.objects.all().filter(categoria="COT").order_by("username")
    vendedores = models.Usuarios.objects.all().filter(categoria="VEN").order_by("username")
    tiempos = {}
    tiempo_promedio_dict = {}
    resultados_dict = {}
    texto_busqueda = ""
    ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
    ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
    ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")
    buscar = "sin busqueda"



    if request.method == "GET":
        buscar = "sin busqueda"
        cot_dict= {}

        ven_dict = {}


        labels = []
        datas = []
        titles = []


        datas_vendedores = []
        titles_vendedores = []

        datas_ot = []
        titles_ot = []


        datas_vendedores_ot = []
        titles_vendedores_ot = []

        datas_ot_gig = []
        titles_ot_gig = []


        datas_vendedores_ot_gig = []
        titles_vendedores_ot_gig = []


        mes = datetime.now().month
        fecha = datetime(datetime.now().year, mes, 1).date()

        fecha -= relativedelta(years=+1)
        fecha_hasta = datetime(datetime.now().year, mes, monthrange(datetime.now().year, mes)[1]).date()

        cotizadores = models.Usuarios.objects.filter(categoria="COT").filter(date_joined__range=[str(fecha),str(fecha_hasta)])
        vendedores = models.Usuarios.objects.filter(categoria="VEN").filter(date_joined__range=[str(fecha),str(fecha_hasta)])

        for i in range(13):
            labels.append(fecha.strftime('%h'))
            fecha_hasta = (fecha + relativedelta(months=+1))



            fecha += relativedelta(months=+1)


        fecha = datetime(datetime.now().year, mes, 1).date()

        fecha -= relativedelta(years=+1)

        for cotizador in cotizadores:
            titles.append(cotizador.username)

        lista = []

        for i in range(len(titles)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(fecha),str(fecha_hasta)]).filter(cotizador__exact=str(titles[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas.append(lista)

        for vendedor in vendedores:
            titles_vendedores.append(vendedor.username)



        for i in range(len(titles_vendedores)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = CotizacionesSolicitadas.objects.filter(fecha_completada__range=[str(fecha),str(fecha_hasta)]).filter(vendedor=str(titles_vendedores[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas_vendedores.append(lista)


        for cotizador in cotizadores:
            titles_ot.append(cotizador.username)

        lista = []

        for i in range(len(titles)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(fecha),str(fecha_hasta)]).filter(cotizador_ot__exact=str(titles[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas_ot.append(lista)

        for vendedor in vendedores:
            titles_vendedores_ot.append(vendedor.username)



        for i in range(len(titles_vendedores)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = OrdenesSolicitadas.objects.filter(fecha_completada_ot__range=[str(fecha),str(fecha_hasta)]).filter(vendedor_ot=str(titles_vendedores[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas_vendedores_ot.append(lista)




        hoy = date.today()
        primero_mes = datetime(datetime.now().year, mes, 1).date()
        primero_año = datetime(datetime.now().year, 1, 1).date()

        lista = []

        for i in range(len(titles)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = models.OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(fecha),str(fecha_hasta)]).filter(cotizador_ot__exact=str(titles[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas_ot_gig.append(lista)

        for vendedor in vendedores:
            titles_vendedores_ot_gig.append(vendedor.username)



        for i in range(len(titles_vendedores)):
            lista = []
            for e in range(13):

                fecha_hasta = (fecha + relativedelta(months=+1))

                busqueda = models.OrdenesGigantografia.objects.filter(fecha_completada_ot__range=[str(fecha),str(fecha_hasta)]).filter(vendedor_ot=str(titles_vendedores[i]))

                lista.append(busqueda.count())

                fecha += relativedelta(months=+1)
            fecha = datetime(datetime.now().year, mes, 1).date()

            fecha -= relativedelta(years=+1)
            datas_vendedores_ot_gig.append(lista)




        hoy = date.today()
        primero_mes = datetime(datetime.now().year, mes, 1).date()
        primero_año = datetime(datetime.now().year, 1, 1).date()

        print(hoy)
        print(primero_año)
        print(primero_mes)

        for cotizador in cotizadores:
            cot_dict[cotizador.username] = {}
            cot_dict[cotizador.username]["hoy"] = models.CotizacionesSolicitadas.objects.all().filter(cotizador__exact=cotizador.username).filter(fecha_completada__range=[hoy,(hoy + timedelta(days=1))]).count()
            cot_dict[cotizador.username]["mes"] = models.CotizacionesSolicitadas.objects.all().filter(cotizador__exact=cotizador.username).filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).count()
            cot_dict[cotizador.username]["año"] = models.CotizacionesSolicitadas.objects.all().filter(cotizador__exact=cotizador.username).filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).count()
            cot_dict[cotizador.username]["hoy ot"] = models.OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).count()
            cot_dict[cotizador.username]["mes ot"] = models.OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).count()
            cot_dict[cotizador.username]["año ot"] = models.OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).count()
            cot_dict[cotizador.username]["hoy ot gig"] = models.OrdenesGigantografia.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).count()
            cot_dict[cotizador.username]["mes ot gig"] = models.OrdenesGigantografia.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).count()
            cot_dict[cotizador.username]["año ot gig"] = models.OrdenesGigantografia.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).count()


            try:
                cot_dict[cotizador.username]["ratio mes"] = str(round((((OrdenesSolicitadas.objects.all().filter(cotizador_ot=cotizador.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(cotizador=cotizador.username).filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
            except ZeroDivisionError:
                cot_dict[cotizador.username]["ratio mes"] = str(0.0) + "%"
            try:
                cot_dict[cotizador.username]["ratio año"] = str(round((((OrdenesSolicitadas.objects.all().filter(cotizador_ot=cotizador.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(cotizador=cotizador.username).filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
            except ZeroDivisionError:
                cot_dict[cotizador.username]["ratio año"] = str(0.0) + "%"
        cot_dict["Total"] = {}
        cot_dict["Total"]["hoy"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador="").count()
        cot_dict["Total"]["mes"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()
        cot_dict["Total"]["año"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()
        cot_dict["Total"]["hoy ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
        cot_dict["Total"]["mes ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
        cot_dict["Total"]["año ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()
        cot_dict["Total"]["hoy ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
        cot_dict["Total"]["mes ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
        cot_dict["Total"]["año ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()


        try:
            cot_dict["Total"]["ratio mes"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()))*100), 2)) + "%"
        except ZeroDivisionError:
            cot_dict["Total"]["ratio mes"] = str(0.0) + "%"
        try:
            cot_dict["Total"]["ratio año"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()))*100), 2)) + "%"
        except ZeroDivisionError:
            cot_dict["Total"]["ratio año"] = str(0.0) + "%"
        for vendedor in vendedores:
            ven_dict[vendedor.username] = {}
            ven_dict[vendedor.username]["hoy"] = CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador="").count()
            ven_dict[vendedor.username]["mes"] = CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()
            ven_dict[vendedor.username]["año"] = CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()
            ven_dict[vendedor.username]["hoy_ot"] = OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
            ven_dict[vendedor.username]["mes_ot"] = OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
            ven_dict[vendedor.username]["año_ot"] = OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()
            ven_dict[vendedor.username]["hoy_ot_gig"] = OrdenesGigantografia.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
            ven_dict[vendedor.username]["mes_ot_gig"] = OrdenesGigantografia.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
            ven_dict[vendedor.username]["año_ot_gig"] = OrdenesGigantografia.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()
            try:
                ven_dict[vendedor.username]["ratio mes"] = str(round((((OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
            except ZeroDivisionError:
                ven_dict[vendedor.username]["ratio mes"] = str(0.0) + "%"
            try:
                ven_dict[vendedor.username]["ratio año"] = str(round((((OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
            except ZeroDivisionError:
                ven_dict[vendedor.username]["ratio año"] = str(0.0) + "%"
        ven_dict["Total"] = {}
        ven_dict["Total"]["hoy"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador="").count()
        ven_dict["Total"]["mes"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()
        ven_dict["Total"]["año"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()
        ven_dict["Total"]["hoy ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
        ven_dict["Total"]["mes ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
        ven_dict["Total"]["año ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()
        ven_dict["Total"]["hoy ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[hoy,(hoy + timedelta(days=1))]).exclude(cotizador_ot="").count()
        ven_dict["Total"]["mes ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count()
        ven_dict["Total"]["año ot gig"] = models.OrdenesGigantografia.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count()
        try:
            ven_dict["Total"]["ratio mes"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_mes,(primero_mes + relativedelta(months=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
        except ZeroDivisionError:
            ven_dict["Total"]["ratio mes"] = str(0.0) + "%"
        try:
            ven_dict["Total"]["ratio año"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[primero_año,(primero_año + relativedelta(years=+1))]).exclude(cotizador="").count()))*100),2)) + "%"
        except ZeroDivisionError:
            ven_dict["Total"]["ratio año"] = str(0.0) + "%"

        print("aqui",cot_dict)
        print(ven_dict)

        ordenes_existentes = OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact="")
        ordenes_proceso = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").order_by("fecha_entrega_ot")
        ordenes_por_fecha = OrdenesSolicitadas.objects.all().exclude(estado_ot__exact="Cerrada").exclude(estado_ot__exact="Por aperturar").filter(fecha_entrega_ot=None).order_by("fecha_entrega_ot")


        return render(request,"reportes.html",{"datas_ot_gig":datas_ot_gig,"datas_vendedores_ot_gig":datas_vendedores_ot_gig,"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"datas_vendedores_ot":datas_vendedores_ot,"titles_vendedores_ot":titles_vendedores_ot,"titles_ot":titles_ot,"datas_ot":datas_ot,"buscar":buscar,"cot_dict":cot_dict,"ven_dict":ven_dict,"ordenes_existentes":ordenes_existentes,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"datas_vendedores":datas_vendedores,"titles_vendedores":titles_vendedores,"titles":titles,"labels_names":labels,"datas":datas,"resultados_dict":resultados_dict,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})

        return render(request,"reportes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"datas_vendedores_ot":datas_vendedores_ot,"titles_vendedores_ot":titles_vendedores_ot,"titles_ot":titles_ot,"datas_ot":datas_ot,"buscar":buscar,"cot_dict":cot_dict,"ven_dict":ven_dict,"ordenes_existentes":ordenes_existentes,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"datas_vendedores":datas_vendedores,"titles_vendedores":titles_vendedores,"titles":titles,"labels_names":labels,"datas":datas,"resultados_dict":resultados_dict,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})


    if request.method == "POST" and request.POST.get("buscar") == "BUSCAR":
        buscar = "True"
        desde = request.POST.get("desde")
        hasta = request.POST.get("hasta")



        #por_cotizador_dict = {}
        #texto_busqueda += "Intervalo de busqueda: " + str(desde) + " hasta " + str(hasta)
        print(type(desde))
        print(hasta)
        cot_dict= {}

        ven_dict = {}

        mes = datetime.now().month
        fecha = datetime(datetime.now().year, mes, 1).date()

        fecha -= relativedelta(years=+1)
        fecha_hasta = datetime(datetime.now().year, mes, monthrange(datetime.now().year, mes)[1]).date()

        cotizadores = models.Usuarios.objects.filter(categoria="COT").filter(date_joined__range=[str(fecha),str(fecha_hasta)])
        vendedores = models.Usuarios.objects.filter(categoria="VEN").filter(date_joined__range=[str(fecha),str(fecha_hasta)])

        for cotizador in cotizadores:
            cot_dict[cotizador.username] = {}

            cot_dict[cotizador.username]["cot"] = models.CotizacionesSolicitadas.objects.all().filter(cotizador__exact=cotizador.username).filter(fecha_completada__range=[desde,hasta]).count()

            cot_dict[cotizador.username]["ot"] = models.OrdenesSolicitadas.objects.all().filter(cotizador_ot__exact=cotizador.username).filter(fecha_completada_ot__range=[desde,hasta]).count()
            try:
                cot_dict[cotizador.username]["ratio"] = str(round((((OrdenesSolicitadas.objects.all().filter(cotizador_ot=cotizador.username).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(cotizador=cotizador.username).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()))*100),2)) + "%"
            except ZeroDivisionError:
                cot_dict[cotizador.username]["ratio"] = str(0.0) + "%"

        cot_dict["Total"] = {}

        cot_dict["Total"]["cot"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()

        cot_dict["Total"]["ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count()
        try:
            cot_dict["Total"]["ratio"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()))*100), 2)) + "%"
        except ZeroDivisionError:
            cot_dict["Total"]["ratio"] = str(0.0) + "%"

        for vendedor in vendedores:
            ven_dict[vendedor.username] = {}

            ven_dict[vendedor.username]["cot"] = CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()

            ven_dict[vendedor.username]["ot"] = OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count()

            try:
                ven_dict[vendedor.username]["ratio"] = str(round(((OrdenesSolicitadas.objects.all().filter(vendedor_ot=vendedor.username).filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(vendedor=vendedor.username).filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count())), 2)*100) + "%"
            except ZeroDivisionError:
                ven_dict[vendedor.username]["ratio"] = str(0.0) + "%"
        ven_dict["Total"] = {}

        ven_dict["Total"]["cot"] = models.CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()

        ven_dict["Total"]["ot"] = models.OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count()

        try:
            ven_dict["Total"]["ratio"] = str(round((((OrdenesSolicitadas.objects.all().filter(fecha_completada_ot__range=[desde,hasta]).exclude(cotizador_ot="").count())/(CotizacionesSolicitadas.objects.all().filter(fecha_completada__range=[desde,hasta]).exclude(cotizador="").count()))*100),2)) + "%"
        except ZeroDivisionError:
            ven_dict["Total"]["ratio"] = str(0.0) + "%"

#AQUI VA LO QUE ESTA EN BORRADOR





    #tiempo_promedio = sum(tiempos)/len(tiempos)
    #print(tiempo_promedio)
    #tiempo_real = "{} horas con {} minutos".format(str(tiempo_promedio//3600),str(int(tiempo_promedio % 60)))
    #print(tiempo_real)
    data = {"ventas":100,"clientes":10}
    return render(request,"reportes.html",{"ordenes_existentes_gig":ordenes_existentes_gig,"ordenes_por_fecha_gig":ordenes_por_fecha_gig,"ordenes_proceso_gig":ordenes_proceso_gig,"buscar":buscar,"cot_dict":cot_dict,"ven_dict":ven_dict,"ordenes_por_confirmar":ordenes_por_confirmar,"ordenes_existentes":ordenes_existentes,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_proceso":ordenes_proceso,"ordenes_por_fecha":ordenes_por_fecha,"ordenes_existentes":ordenes_existentes,"data":data,"texto_busqueda":texto_busqueda,"resultados_dict":resultados_dict,"clientes_creados":clientes_creados,"trabajos_creados":trabajos_creados,"cotizadores":cotizadores,"vendedores":vendedores,"cotizaciones_existentes":cotizaciones_existentes})
