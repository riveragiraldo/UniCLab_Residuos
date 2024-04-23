from django.db import models
from reactivos.models import User

# Modelo Clasificación de residuos
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
