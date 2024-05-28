from django.db import models
from reactivos.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# -------------------------------- #
# Modelo Clasificación de residuos #
class CLASIFICACION_RESIDUOS(models.Model):
    name = models.CharField(
        max_length=10,
        verbose_name="Nombre",
        help_text="Máximo 10 caracteres",
        unique=True,
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Descripción",
        help_text="Máximo 500 caracteres",
        unique=False,
    )
    is_active = models.BooleanField(
        verbose_name="Activo",
        help_text="Activo",
        default=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_clasificacion",
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha Creación",
        null=True,
        blank=True,
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha Actualización",
        null=True,
        blank=True,
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Actualizado por",
        related_name="updateby_clasificacion",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Clasificación de Residuos"
        verbose_name_plural = "Clasificaciones de Residuos"


# -----------------------_ #
# Modelo solicitud Residuo #
class SOLICITUD_RESIDUO(models.Model):
    name = models.CharField(max_length=14, default="Sol")
    leido = models.BooleanField(
        verbose_name="Leído",
        help_text="Leído",
        default=False,
    )
    respondido = models.BooleanField(
        verbose_name="Respondido",
        help_text="Respondido",
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name="Activo",
        help_text="Activo",
        default=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_solicitud_residuo",
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha Creación",
        null=True,
        blank=True,
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha Actualización",
        null=True,
        blank=True,
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Actualizado por",
        related_name="updateby_solicitud_residuo",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Registro de Residuo"
        verbose_name_plural = "Registros de Residuos"


# --------------------------- #
# Modelo Registro de residuos #
class REGISTRO_RESIDUOS(models.Model):
    DEPENDENCIA_CHOICES = [
        ("Area", "ÁREA"),
        ("Laboratorio", "LABORATORIO"),
    ]
    registro_solicitud = models.ForeignKey(
        SOLICITUD_RESIDUO,
        related_name="solicitud_residuos",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    dependencia = models.CharField(
        max_length=11, choices=DEPENDENCIA_CHOICES, verbose_name="Dependencia"
    )
    area = models.CharField(max_length=200, blank=True, null=True)
    laboratorio = models.ForeignKey(
        "reactivos.Laboratorios", on_delete=models.SET_NULL, null=True, blank=True
    )
    nombre_residuo = models.CharField(max_length=400, verbose_name="Nombre del Residuo")
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cantidad",
        validators=[MinValueValidator(0)],
    )
    unidades = models.ForeignKey(
        "reactivos.Unidades", on_delete=models.CASCADE, verbose_name="Unidades"
    )
    numero_envases = models.PositiveIntegerField(
        verbose_name="Número de Envases",
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    clasificado = models.ManyToManyField(
        "CLASIFICACION_RESIDUOS",
        verbose_name="Clasificado",
        blank=True,
    )
    estado = models.ForeignKey(
        "reactivos.Estados", on_delete=models.CASCADE, verbose_name="Estado"
    )
    observaciones = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Observaciones"
    )
    residuo_enviado = models.BooleanField(
        verbose_name="Estado de envío",
        help_text="Estado de envío de solicitud al servidor",
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name="Activo", help_text="Activo", default=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_registro",
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
        related_name="updateby_registro",
    )

    # Campo para el total
    total_residuo = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name="Total", blank=True, null=True
    )

    def __str__(self):
        return self.nombre_residuo

    class Meta:
        verbose_name = "Registro de Residuos"
        verbose_name_plural = "Registros de Residuos"


# Modelo fichas de seguirdad
class FichaSeguridad(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Nombre de Ficha o Proveedor"
    )
    url = models.URLField(max_length=500, verbose_name="URL", unique=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_fichaseguiridad",
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
        related_name="updateby_fichaseguiridad",
    )
    is_active = models.BooleanField(
        verbose_name="Activo", help_text="Activo", default=True
    )

    class Meta:
        verbose_name = "Ficha de Seguridad"
        verbose_name_plural = "Fichas de Seguridad"

    def __str__(self):
        return self.name


# ---------------------------------- #
# Modelo Certificados de disposición #
# Función para validar el tamaño del archivo


def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("El tamaño máximo del archivo es 2MB")


class CERTIFICADO_DISPOSICION(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name="Descripción breve"
    )
    date = models.DateField(verbose_name="Fecha de Certificación")
    attach = models.FileField(
        upload_to="certificados_finales/",
        verbose_name="Adjunto",
        validators=[
            FileExtensionValidator(["pdf", "doc", "docx", "jpg", "jpeg", "png"]),
            validate_file_size,
        ],
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_certificadodisposicion",
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
        related_name="updateby_certificadodisposicion",
    )
    is_active = models.BooleanField(
        verbose_name="Activo", help_text="Activo", default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Certificado de Disposición"
        verbose_name_plural = "Certificados de Disposición"

class InformacionInteres(models.Model):
    TIPO_CHOICES = [
        ('Video de Youtube', 'Video de Youtube'),
        ('Enlace Externo', 'Enlace Externo'),
    ]

    name = models.CharField(max_length=150, unique=True, verbose_name="Breve descripción o Título")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    url = models.URLField(unique=True, verbose_name="URL", max_length=500)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name="createby_enlaces",
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
        related_name="updateby_enlaces",
    )
    is_active = models.BooleanField(
        verbose_name="Activo", help_text="Activo", default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Información de Interés"
        verbose_name_plural = "Información de Interés"
