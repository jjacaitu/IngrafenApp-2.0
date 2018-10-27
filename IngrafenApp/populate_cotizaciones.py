import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","IngrafenApp.settings")

import django
django.setup()

import random
from cotizacion.models import CotizacionesSolicitadas,TipoDeTrabajo,Clientes,Materiales
from faker import Faker

fakegen = Faker()
