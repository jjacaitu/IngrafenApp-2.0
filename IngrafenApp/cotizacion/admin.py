from django.contrib import admin
from cotizacion.models import Usuarios,Materiales,CotizacionesSolicitadas, TipoDeTrabajo, Clientes

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(CotizacionesSolicitadas)
admin.site.register(TipoDeTrabajo)
admin.site.register(Materiales)
admin.site.register(Clientes)
