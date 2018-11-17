# Generated by Django 2.1 on 2018-11-17 21:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes_ot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_razon_social', models.CharField(max_length=40)),
                ('vendedor_asociado', models.CharField(blank=True, max_length=20)),
                ('usuario', models.CharField(blank=True, max_length=20)),
                ('codigo', models.CharField(max_length=20)),
                ('desactivado', models.BooleanField(default=False)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_razon_social', to='cotizacion.Clientes')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenesSolicitadas',
            fields=[
                ('num_solicitud_ot', models.AutoField(primary_key=True, serialize=False)),
                ('vendedor_ot', models.CharField(blank=True, max_length=20)),
                ('trabajo_ot', models.CharField(max_length=40)),
                ('tipo_trabajo_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('cantidad_ot', models.IntegerField()),
                ('material_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('descripcion_material_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('medida_alto_ot', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_ot', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('impresion_tiro_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('impresion_retiro_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('uv_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('laminado_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('troquelado_ot', models.CharField(blank=True, max_length=30, null=True)),
                ('material2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_2_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_2_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado2_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_3_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_3_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado3_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_4_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_4_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado4_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_5_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_5_ot', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado5_ot', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('fecha_solicitada_ot', models.DateTimeField(auto_now_add=True)),
                ('detalles_ot', models.CharField(blank=True, max_length=300, null=True)),
                ('fecha_completada_ot', models.DateTimeField(blank=True, null=True)),
                ('cotizador_ot', models.CharField(blank=True, max_length=20)),
                ('numero_cotizacion_ot', models.CharField(blank=True, max_length=20)),
                ('fecha_entrega_ot', models.DateField(blank=True, null=True)),
                ('fecha_entregada', models.DateField(blank=True, null=True)),
                ('procesado_por_ot', models.CharField(blank=True, default=' ', max_length=25)),
                ('estado_ot', models.CharField(blank=True, default='Por aperturar', max_length=25)),
                ('num_ot_relacionada', models.CharField(blank=True, default='', max_length=20)),
                ('solicitud_cot', models.CharField(blank=True, default='', max_length=20)),
                ('direccion_entrega', models.CharField(blank=True, max_length=50)),
                ('persona_recibe', models.CharField(blank=True, max_length=20)),
                ('forma_empaque', models.CharField(blank=True, max_length=20)),
                ('arte', models.BooleanField(default=False)),
                ('dummie', models.BooleanField(default=False)),
                ('machote', models.BooleanField(default=False)),
                ('prueba_de_color', models.BooleanField(default=False)),
                ('muestra_real', models.BooleanField(default=False)),
                ('precio_ot', models.FloatField(blank=True, default=0, null=True)),
                ('material_confirmado', models.BooleanField(default=False)),
                ('tipo_impresion', models.CharField(choices=[('Offset', 'Impresion Offset'), ('Laser', 'Impresion Laser')], max_length=10)),
                ('nombre_cliente_ot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_ot', to='cotizacion.Clientes_ot')),
            ],
        ),
    ]
