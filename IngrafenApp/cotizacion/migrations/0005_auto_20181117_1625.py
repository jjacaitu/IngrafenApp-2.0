# Generated by Django 2.1 on 2018-11-17 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotizacion', '0004_auto_20181117_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes_ot',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='ordenessolicitadas',
            name='nombre_cliente_ot',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='nombre_razon_social',
        ),
        migrations.RemoveField(
            model_name='cotizacionessolicitadas',
            name='aprobacion_cot',
        ),
        migrations.DeleteModel(
            name='Clientes_ot',
        ),
        migrations.DeleteModel(
            name='OrdenesSolicitadas',
        ),
    ]
