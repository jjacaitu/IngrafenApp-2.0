# Generated by Django 2.1.1 on 2018-11-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizacion', '0003_ordenessolicitadas_fecha_entregada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes_ot',
            name='codigo',
            field=models.CharField(max_length=20),
        ),
    ]
