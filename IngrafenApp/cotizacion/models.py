from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator
from django import forms
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.

IMPRESION_CHOICES = (("NO","Sin impresion"),("FCT","Full color tiro"),("FCTR","Full color tiro y retiro"),("PT","Pantone Tiro"),("PTR","Pantone Tiro y Retiro"))
TIPO_PR_CHOICES = (("OF","OFFSET"),("G","GIGANTOGRAFIA"),("OF","OFFSET Y GIGANTOGRAFIA"))
CATEGORIA_USUARIO = (("ADM","ADMINISTRADOR"),("VEN","VENDEDOR"),("COT","COTIZADOR"),("PRO","PRODUCCION"),("DIS","DISEÑO"))
UV_CHOICES = (("SIN","SIN UV"),("UVT","UV TIRO"),("UVTR","UV TIRO Y RETIRO"),("UVST","UV SECTORIZADO TIRO"),("UVSTR","UV SECTORIZADO TIRO Y RETIRO"))
LAMINADO_CHOICES = (("SIN","SIN LAMINADO"),("LBT","LAMINADO BRILLO TIRO"),("LBTR","LAMINADO BRILLO TIRO Y RETIRO"),("LMT","LAMINADO MATE TIRO"),("LMTR","LAMINADO MATE TIRO Y RETIRO"))
TROQUELADO_CHOICES = (("SIN","SIN TROQUELAR"),("TRN","TROQUEL NUEVO"),("TRE","TROQUEL EXISTENTE"),("MC","EN PLANAS CON MEDIO CORTE"))


class Usuarios(AbstractUser):
    categoria = models.CharField(max_length=3,choices=CATEGORIA_USUARIO,default="ADM")


class Materiales(models.Model):
    material = models.CharField(max_length=40, unique=True)
    usuario = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.material

    def save(self):
       self.material = self.material.title()
       super(Materiales, self).save()
    #COLOCAR OTROS ASPECTOS DE VENDEDOR

class TipoDeTrabajo(models.Model):
    trabajo = models.CharField(max_length=40, unique=True)
    materiales_adicionales = models.BooleanField(default=False)
    insumo = models.CharField(max_length=20,blank=True)
    usuario = models.CharField(max_length=20, blank=True)

    def save(self):
       self.trabajo = self.trabajo.title()
       super(TipoDeTrabajo, self).save()

    def __str__(self):
        return self.trabajo

class Clientes(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    vendedor_asociado = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    usuario = models.CharField(max_length=20, blank=True)
    def save(self):
       self.nombre = self.nombre.title()
       super(Clientes, self).save()

    def __str__(self):
        return self.nombre

class CotizacionesSolicitadas(models.Model):
    num_solicitud = models.AutoField(primary_key = True)
    vendedor = models.CharField(max_length=20, blank=True)
    trabajo = models.CharField(max_length=40)
    nombre_cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT, related_name="client")
    tipo_trabajo = models.CharField(max_length=30,null=True,blank=True)
    cantidad = models.IntegerField()

    material = models.CharField(max_length=30,null=True,blank=True)
    descripcion_material = models.CharField(max_length=30,null=True,blank=True)
    medida_alto = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)])
    medida_ancho = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)])
    impresion_tiro = models.CharField(max_length=30,null=True,blank=True)
    impresion_retiro = models.CharField(max_length=30,null=True,blank=True)
    uv = models.CharField(max_length=30,null=True,blank=True)
    laminado = models.CharField(max_length=30,null=True,blank=True)
    troquelado = models.CharField(max_length=30,null=True,blank=True)

    material2 = models.CharField(max_length=30,null=True,blank=True,default="")
    medida_alto_2 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    medida_ancho_2 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    descripcion_material2 = models.CharField(max_length=30,null=True,blank=True,default="")
    impresion_tiro2 = models.CharField(max_length=30,null=True,blank=True,default="")
    impresion_retiro2 = models.CharField(max_length=30,null=True,blank=True,default="")
    uv2 = models.CharField(max_length=30,null=True,blank=True,default="")
    laminado2 = models.CharField(max_length=30,null=True,blank=True,default="")
    troquelado2 = models.CharField(max_length=30,null=True,blank=True,default="")

    material3 = models.CharField(max_length=30,null=True,blank=True,default="")
    medida_alto_3 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    medida_ancho_3 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    descripcion_material3 = models.CharField(max_length=30,null=True,blank=True,default="")
    impresion_tiro3 = models.CharField(max_length=30,null=True,blank=True,default="")
    impresion_retiro3 = models.CharField(max_length=30,null=True,blank=True,default="")
    uv3 = models.CharField(max_length=30,null=True,blank=True,default="")
    laminado3 = models.CharField(max_length=30,null=True,blank=True,default="")
    troquelado3 = models.CharField(max_length=30,null=True,blank=True,default="")

    material4 = models.CharField(max_length=30,null=True,blank=True, default="")
    medida_alto_4 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    medida_ancho_4 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)], default=0)
    descripcion_material4 = models.CharField(max_length=30,null=True,blank=True, default="")
    impresion_tiro4 = models.CharField(max_length=30,null=True,blank=True, default="")
    impresion_retiro4 = models.CharField(max_length=30,null=True,blank=True, default="")
    uv4 = models.CharField(max_length=30,null=True,blank=True, default="")
    laminado4 = models.CharField(max_length=30,null=True,blank=True, default="")
    troquelado4 = models.CharField(max_length=30,null=True,blank=True, default="")

    material5 = models.CharField(max_length=30,null=True,blank=True, default="")
    medida_alto_5 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)],default=0)
    medida_ancho_5 = models.FloatField(null=True,blank=True,validators=[MaxValueValidator(99)],default=0)
    descripcion_material5 = models.CharField(max_length=30,null=True,blank=True, default="")
    impresion_tiro5 = models.CharField(max_length=30,null=True,blank=True, default="")
    impresion_retiro5 = models.CharField(max_length=30,null=True,blank=True, default="")
    uv5 = models.CharField(max_length=30,null=True,blank=True, default="")
    laminado5 = models.CharField(max_length=30,null=True,blank=True, default="")
    troquelado5 = models.CharField(max_length=30,null=True,blank=True, default="")


    cantidad2 = models.IntegerField(null=True, blank=True, default=0)
    cantidad3 = models.IntegerField(null=True, blank=True, default =0)

    fecha_solicitada = models.DateTimeField(auto_now_add=True)

    detalles = models.CharField(max_length=300, blank=True,null=True)
    fecha_completada = models.DateTimeField(auto_now=True)
    cotizador = models.CharField(max_length=20, blank=True)
    numero_cotizacion = models.CharField(max_length=20, blank=True)
    imagen = models.ImageField(upload_to="uploads/", blank=True, null=True, default="none")
    procesado_por = models.CharField(max_length=25,default=" ",blank=True)

    solicitud_ot = models.CharField(max_length=20, blank=True, default= "")
    num_ot_relacionada = models.CharField(max_length=20, blank=True, default= "")
#AUMENTAR PARA SUBIR IMAGEN DE LO QUE SE DESEA COTIZAR

    def save(self, *args, **kwargs):
        if not self.num_solicitud:
            if self.imagen != "none":
                self.imagen = self.compressImage(self.imagen)

        super(CotizacionesSolicitadas, self).save(*args, **kwargs)

    def compressImage(self,imagen):
        imageTemporary = Image.open(imagen)
        outputIoStream = BytesIO()
        imageTemporaryResized = imageTemporary.resize( (1020,573) )
        imageTemporary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        ultima_solicitud = CotizacionesSolicitadas.objects.all().last()
        if ultima_solicitud == None:
            imagen = InMemoryUploadedFile(outputIoStream,'ImageField', "solicitud # %s.jpg" % (1), 'image/jpeg', sys.getsizeof(outputIoStream), None)
        else:
            imagen = InMemoryUploadedFile(outputIoStream,'ImageField', "solicitud # %s.jpg" % (ultima_solicitud.num_solicitud + 1), 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return imagen



    def __str__(self):
        return "#{},cliente: {},trabajo: {}".format(str(self.num_solicitud),str(self.nombre_cliente),str(self.tipo_trabajo))

#CAMBIAR EL MODELO
