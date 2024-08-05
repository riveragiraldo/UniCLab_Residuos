from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from reactivos.models import *

# Create your models here.

from django.db import models

# --------------------- #
# Modelo de advertencia #
class Advertencia(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Advertencia"
        verbose_name_plural = "Advertencias"


# --------------- #
# Modelo Frases H #
class Frases_H(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Frase H"
        verbose_name_plural = "Frases H"

# --------------- #
# Modelo Frases P #
class Frases_P(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Frase P"
        verbose_name_plural = "Frases P"



# ----------------- #
# Modelo Pictograma #

def validate_image_extension(value):
    if not value.name.endswith('.png'):
        raise ValidationError(_('El archivo debe tener la extensión .png.'))

def validate_image_size(value):
    limit_kb = 100
    if value.size > limit_kb * 1024:
        raise ValidationError(_('El archivo no debe superar los 100 KB.'))

def validate_image_dimensions(value):
    image = Image.open(value)
    width, height = image.size
    if width != height:
        raise ValidationError(_('La imagen debe ser simétrica (ancho y altura deben ser iguales).'))


class Pictograma(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    pictogram = models.ImageField(
        upload_to='pictogramas/',
        verbose_name="Pictograma",
        validators=[validate_image_extension, validate_image_size, validate_image_dimensions]
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_pictogramas",
    )
    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha Creación", null=True, blank=True
    )
    last_update = models.DateTimeField(
        auto_now=True, verbose_name="Fecha Actualización", null=True, blank=True
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Actualizado por",
        related_name="updateby_pictogramas",
    )
    is_active = models.BooleanField(
        verbose_name="Activo", help_text="Activo", default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pictograma"
        verbose_name_plural = "Pictogramas"



# ----------------- #
# Modelo Sustancias #
class Sustancias(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150)
    cas = models.CharField(verbose_name='CAS', max_length=40, blank=True, null=True)
    warning = models.ForeignKey(Advertencia, verbose_name='Advertencia', on_delete=models.SET_NULL, blank=True, null=True)
    phrase_h = models.ManyToManyField(Frases_H, verbose_name='Frases H', blank=True)
    phrase_p = models.ManyToManyField(Frases_P, verbose_name='Frases P', blank=True)
    pictogram_clp1 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 1', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp1')
    pictogram_clp2 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 2', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp2')
    pictogram_clp3 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 3', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp3')
    pictogram_clp4 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 4', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp4')
    pictogram_clp5 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 5', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp5')
    pictogram_clp6 = models.ForeignKey(Pictograma, verbose_name='Pictograma CLP 6', on_delete=models.SET_NULL, blank=True, null=True, related_name='pictograma_clp6')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"