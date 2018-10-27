from django import forms
from django.forms import ModelForm
from cotizacion.models import Usuarios,CotizacionesSolicitadas, Materiales, TipoDeTrabajo, Clientes
from cotizacion import views, models


class Crear_usuario(ModelForm):
    class Meta:
         model = Usuarios
         fields = ("username", "first_name","last_name","password", "email", "categoria")

class Materiales(ModelForm):
    class Meta:
        model = Materiales
        exclude = ["usuario"]

class TipoDeTrabajo(ModelForm):
    class Meta:
        model = TipoDeTrabajo
        exclude = ["usuario"]

class Clientes(ModelForm):
    class Meta:
        model = Clientes
        exclude = ["usuario"]

    def __init__(self, *args, **kwargs):
        super(Clientes, self).__init__(*args, **kwargs)
        self.fields['vendedor_asociado'].queryset = Usuarios.objects.filter(categoria="VEN") | Usuarios.objects.filter(categoria="ADM")


class Solicitud_cot(ModelForm):
    class Meta:
        model = CotizacionesSolicitadas
        exclude = ["vendedor","cotizador","numero_cotizacion"]

    def __init__(self,user, *args, **kwargs):
        super(Solicitud_cot, self).__init__(*args, **kwargs)
        self.fields['nombre_cliente'].queryset = models.Clientes.objects.filter(vendedor_asociado=user)
        #widgets = {"impresion":forms.RadioSelect(),"uv":forms.RadioSelect(),"laminado":forms.RadioSelect(),"troquelado":forms.RadioSelect()}
