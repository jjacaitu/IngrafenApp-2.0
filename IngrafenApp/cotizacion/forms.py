from django import forms
from django.forms import ModelForm
from cotizacion.models import Usuarios,CotizacionesSolicitadas, Materiales, TipoDeTrabajo, Clientes, OrdenesSolicitadas, Clientes_ot, Materiales_gig, TipoDeTrabajo_gig, OrdenesGigantografia
from cotizacion import views, models


class Crear_usuario(ModelForm):
    class Meta:
         model = Usuarios
         fields = ("username", "first_name","last_name","password", "email", "categoria")

class Materiales(ModelForm):
    class Meta:
        model = Materiales
        exclude = ["usuario"]

class Materiales_gig(ModelForm):
    class Meta:
        model = Materiales_gig
        exclude = ["usuario"]

class TipoDeTrabajo(ModelForm):
    class Meta:
        model = TipoDeTrabajo
        exclude = ["usuario"]

class TipoDeTrabajo_gig(ModelForm):
    class Meta:
        model = TipoDeTrabajo_gig
        exclude = ["usuario"]

class Clientes(ModelForm):
    class Meta:
        model = Clientes
        exclude = ["usuario","nombre_razon_social","desactivado"]

    def __init__(self, *args, **kwargs):
        super(Clientes, self).__init__(*args, **kwargs)
        self.fields['vendedor_asociado'].queryset = Usuarios.objects.filter(categoria="VEN") | Usuarios.objects.filter(categoria="ADM")

class Clientes_ot(ModelForm):
    class Meta:
        model = Clientes_ot
        exclude = ["usuario","vendedor_asociado","desactivado"]

    def __init__(self,user, *args, **kwargs):
        super(Clientes_ot, self).__init__(*args, **kwargs)
        self.fields['nombre'].queryset = models.Clientes.objects.filter(nombre_razon_social="").order_by("nombre")

class Solicitud_cot(ModelForm):
    class Meta:
        model = CotizacionesSolicitadas
        exclude = ["vendedor","cotizador","numero_cotizacion"]

    def __init__(self,user, *args, **kwargs):
        super(Solicitud_cot, self).__init__(*args, **kwargs)
        self.fields['nombre_cliente'].queryset = models.Clientes.objects.filter(vendedor_asociado=user,desactivado=False).order_by("nombre")
        #widgets = {"impresion":forms.RadioSelect(),"uv":forms.RadioSelect(),"laminado":forms.RadioSelect(),"troquelado":forms.RadioSelect()}
class Solicitud_ot(ModelForm):
    class Meta:
        model = OrdenesSolicitadas
        exclude = ["vendedor_ot","cotizador_ot","numero_cotizacion_ot","fecha_entrega_ot"]
        #widgets = {"tipo_impresion":forms.RadioSelect()}
    def __init__(self,user, *args, **kwargs):
        super(Solicitud_ot, self).__init__(*args, **kwargs)
        self.fields['nombre_cliente_ot'].queryset = models.Clientes_ot.objects.filter(vendedor_asociado=user,desactivado=False).order_by("nombre_razon_social")

class Solicitud_ot_aprobacion(ModelForm):
    class Meta:
        model = OrdenesSolicitadas
        exclude = ["vendedor_ot","cotizador_ot","numero_cotizacion_ot","fecha_entrega_ot"]
        #widgets = {"tipo_impresion":forms.RadioSelect()}
    def __init__(self,user, *args, **kwargs):
        super(Solicitud_ot_aprobacion, self).__init__(*args, **kwargs)


class Solicitud_ot_gig(ModelForm):
    class Meta:
        model = OrdenesGigantografia
        exclude = ["vendedor_ot","cotizador_ot","numero_cotizacion_ot","fecha_entrega_ot"]
        widgets = {"tipo_impresion":forms.RadioSelect()}
    def __init__(self,user, *args, **kwargs):
        super(Solicitud_ot_gig, self).__init__(*args, **kwargs)
        self.fields['nombre_cliente_ot'].queryset = models.Clientes_ot.objects.filter(vendedor_asociado=user,desactivado=False).order_by("nombre_razon_social")
#lass Bloqueo_cliente(ModelForm):
#    class Meta:
#        model = Clientes_ot
#        exclude = ["usuario","vendedor_asociado","codigo"]
#
#    def __init__(self,user, *args, **kwargs):
#        super(Clientes_ot, self).__init__(*args, **kwargs)
#        self.fields['nombre'].queryset = models.Clientes.objects.filter(nombre_razon_social="").order_by("nombre")
