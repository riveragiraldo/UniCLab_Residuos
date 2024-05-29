from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *
from django.views.generic import TemplateView
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# -------------------------------------------------------------- #
# Resource para la importación de clasificaciones desde el Admin #
class ClasificacionResources(resources.ModelResource):
    class Meta:
        model = CLASIFICACION_RESIDUOS


# --------------------------------------------------------- #
# Inclusión del modelo clasificación de residuos en el Admin #
@admin.register(CLASIFICACION_RESIDUOS)
class Clasificacionesadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name','description', 'id','created_by','date_create','last_update','last_updated_by',)
    list_filter=('name','description',)
    search_fields=('name','description',)
    list_per_page=10
    ordering=('name',)
    resource_class = ClasificacionResources

# --------------------------------------------------------- #
# Inclusión del modelo registro de residuos en el Admin #
@admin.register(REGISTRO_RESIDUOS)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'residuo_enviado','registro_solicitud', 'created_by','dependencia', 'area', 'laboratorio', 'nombre_residuo', 'cantidad', 'unidades', 'numero_envases', 'total_residuo','clasificado_list', 'estado', 'observaciones','is_active', 'date_create', 'last_update', 'last_updated_by',)
    list_filter = ('nombre_residuo',)
    search_fields = ('nombre_residuo',)
    list_per_page = 10
    ordering = ('id',)
    resource_class = ClasificacionResources

    def clasificado_list(self, obj):
        return ', '.join([str(clasificacion) for clasificacion in obj.clasificado.all()])
    
    clasificado_list.short_description = 'Clasificado'

# ---------------------------------------------------- #
# Inclusión del modelo fichas de seguridad en el Admin #
@admin.register(FichaSeguridad)
class FichasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name','url', 'id',)
    list_filter=('name','url',)
    search_fields=('name','url',)
    list_per_page=10
    ordering=('id',)


# ----------------------------------------------------------- #
# Inclusión del modelo Certificado de disposición en el Admin #
@admin.register(CERTIFICADO_DISPOSICION)
class CertificadosAdmin(admin.ModelAdmin):
    list_display = ('formatted_date', 'name', 'attach',)
    list_filter = ('name', 'date',)
    search_fields = ('name', 'date',)
    list_per_page = 10
    ordering = ('id',)

    def formatted_date(self, obj):
        return obj.date.strftime('%d/%m/%Y')
    formatted_date.admin_order_field = 'date'  # Permite ordenar por fecha
    formatted_date.short_description = 'Fecha'

# ----------------------------------------------------------- #
# Inclusión del modelo InformacionInteres en el Admin #
@admin.register(InformacionInteres)
class MaterialInteresAdmin(admin.ModelAdmin):
    list_display = ('name', 'tipo', 'url','id_youtube')
    list_filter = ('name', )
    search_fields = ('name', )
    list_per_page = 10
    ordering = ('id',)

    