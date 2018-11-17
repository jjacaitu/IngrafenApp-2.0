# Generated by Django 2.1 on 2018-11-17 21:15

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('categoria', models.CharField(choices=[('ADM', 'ADMINISTRADOR'), ('VEN', 'VENDEDOR'), ('COT', 'COTIZADOR'), ('PRO', 'PRODUCCION'), ('DIS', 'DISEÑO')], default='ADM', max_length=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, unique=True)),
                ('nombre_razon_social', models.CharField(max_length=40)),
                ('usuario', models.CharField(blank=True, max_length=20)),
                ('desactivado', models.BooleanField(default=False)),
                ('vendedor_asociado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionesSolicitadas',
            fields=[
                ('num_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('vendedor', models.CharField(blank=True, max_length=20)),
                ('trabajo', models.CharField(max_length=40)),
                ('tipo_trabajo', models.CharField(blank=True, max_length=30, null=True)),
                ('cantidad', models.IntegerField()),
                ('material', models.CharField(blank=True, max_length=30, null=True)),
                ('descripcion_material', models.CharField(blank=True, max_length=30, null=True)),
                ('medida_alto', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('impresion_tiro', models.CharField(blank=True, max_length=30, null=True)),
                ('impresion_retiro', models.CharField(blank=True, max_length=30, null=True)),
                ('uv', models.CharField(blank=True, max_length=30, null=True)),
                ('laminado', models.CharField(blank=True, max_length=30, null=True)),
                ('troquelado', models.CharField(blank=True, max_length=30, null=True)),
                ('material2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_2', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_2', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado2', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_3', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_3', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado3', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_4', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_4', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado4', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('material5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('medida_alto_5', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('medida_ancho_5', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('descripcion_material5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_tiro5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('impresion_retiro5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('uv5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('laminado5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('troquelado5', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('cantidad2', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad3', models.IntegerField(blank=True, default=0, null=True)),
                ('fecha_solicitada', models.DateTimeField(auto_now_add=True)),
                ('detalles', models.CharField(blank=True, max_length=300, null=True)),
                ('fecha_completada', models.DateTimeField(blank=True, null=True)),
                ('cotizador', models.CharField(blank=True, max_length=20)),
                ('numero_cotizacion', models.CharField(blank=True, max_length=20)),
                ('imagen', models.ImageField(blank=True, default='none', null=True, upload_to='uploads/')),
                ('procesado_por', models.CharField(blank=True, default=' ', max_length=25)),
                ('solicitud_ot', models.CharField(blank=True, default='', max_length=35)),
                ('num_ot_relacionada', models.CharField(blank=True, default='', max_length=20)),
                ('aprobacion_cot', models.CharField(blank=True, default='Pendiente', max_length=20)),
                ('nombre_cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client', to='cotizacion.Clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Materiales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=40, unique=True)),
                ('usuario', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabajo', models.CharField(max_length=40, unique=True)),
                ('materiales_adicionales', models.BooleanField(default=False)),
                ('insumo', models.CharField(blank=True, max_length=20)),
                ('usuario', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
