from django.contrib import admin
from cotizacion.models import Usuarios,Materiales,CotizacionesSolicitadas, TipoDeTrabajo, Clientes, OrdenesSolicitadas, Clientes_ot, OrdenesGigantografia

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(CotizacionesSolicitadas)
admin.site.register(TipoDeTrabajo)
admin.site.register(Materiales)
admin.site.register(Clientes)
admin.site.register(OrdenesSolicitadas)
admin.site.register(Clientes_ot)
admin.site.register(OrdenesGigantografia)
