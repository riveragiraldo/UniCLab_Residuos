from django.db import models
from reactivos.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# -------------------------------- #
# Modelo Clasificación de residuos #
class CLASIFICACION_RESIDUOS(models.Model):
    name = models.CharField(max_length=10, verbose_name='Nombre', help_text='Máximo 10 caracteres', unique=True)
    description = models.TextField(max_length=500, verbose_name='Descripción', help_text='Máximo 500 caracteres', unique=False)
    is_active = models.BooleanField(verbose_name='Activo', help_text='Activo', default=True,)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Creado por', related_name='createby_clasificacion',)
    date_create = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación', null=True, blank=True,)
    last_update = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización', null=True, blank=True,)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Actualizado por', related_name='updateby_clasificacion',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Clasificación de Residuos'
        verbose_name_plural = 'Clasificaciones de Residuos'


# --------------------------- #
# Modelo Registro de residuos #

class REGISTRO_RESIDUOS(models.Model):
    DEPENDENCIA_CHOICES = [
        
        ('Area', 'ÁREA'),
        ('Laboratorio', 'LABORATORIO'),
    ]

    dependencia = models.CharField(max_length=11, choices=DEPENDENCIA_CHOICES, verbose_name='Dependencia')
    area = models.CharField(max_length=200, blank=True, null=True)
    laboratorio = models.ForeignKey('reactivos.Laboratorios', on_delete=models.SET_NULL, null=True, blank=True)
    nombre_residuo = models.CharField(max_length=400, verbose_name='Nombre del Residuo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad', validators=[MinValueValidator(0)])
    unidades = models.ForeignKey('reactivos.Unidades', on_delete=models.CASCADE, verbose_name='Unidades')
    numero_envases = models.PositiveIntegerField(verbose_name='Número de Envases', default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    clasificado = models.ManyToManyField('CLASIFICACION_RESIDUOS', verbose_name='Clasificado', blank=True, )
    estado = models.ForeignKey('reactivos.Estados', on_delete=models.CASCADE, verbose_name='Estado')
    observaciones = models.CharField(max_length=200, blank=True, null=True, verbose_name='Observaciones')
    is_active = models.BooleanField(verbose_name='Activo', help_text='Activo', default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Creado por', related_name='createby_registro')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación', null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización', null=True, blank=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Actualizado por', related_name='updateby_registro')

    # Campo para el total
    total_residuo = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total', blank=True, null=True)

    def __str__(self):
        return self.nombre_residuo

    

    class Meta:
        verbose_name = 'Registro de Residuos'
        verbose_name_plural = 'Registros de Residuos'

# --------------------------------------------------------------------------- #
# Campo para almacenar una o más fichas de seguridad por registro de residuos #
class FICHAS_SEGURIDAD(models.Model):
    registro_residuo = models.ForeignKey(REGISTRO_RESIDUOS, related_name='archivos_adjuntos_residuos', on_delete=models.CASCADE)
    file = models.FileField(upload_to='archivos/', blank=True, null=True, verbose_name='Ficha de seguiridad')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación', null=True, blank=True)