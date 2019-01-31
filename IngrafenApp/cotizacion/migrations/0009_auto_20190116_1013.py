# Generated by Django 2.1.1 on 2019-01-16 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizacion', '0008_materiales_gig_ordenesgigantografia_tipodetrabajo_gig'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarios',
            old_name='cotizaciones_borradas',
            new_name='cotizaciones_borradas_mes',
        ),
        migrations.RenameField(
            model_name='usuarios',
            old_name='ordenes_borradas',
            new_name='cotizaciones_borradas_totales',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='fecha_ultima_cot',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='fecha_ultima_ot',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='ordenes_borradas_mes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='ordenes_borradas_totales',
            field=models.IntegerField(default=0),
        ),
    ]