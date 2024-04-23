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
class Reactivosadmin(ImportExportModelAdmin, admin.ModelAdmin):
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
    list_display = ('id', 'dependencia', 'area', 'laboratorio', 'nombre_residuo', 'cantidad', 'unidades', 'numero_envases', 'clasificado_list', 'estado', 'is_active', 'created_by', 'date_create', 'last_update', 'last_updated_by',)
    list_filter = ('nombre_residuo',)
    search_fields = ('nombre_residuo',)
    list_per_page = 10
    ordering = ('id',)
    resource_class = ClasificacionResources

    def clasificado_list(self, obj):
        return ', '.join([str(clasificacion) for clasificacion in obj.clasificado.all()])
    
    clasificado_list.short_description = 'Clasificado'