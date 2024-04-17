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

class ClasificacionResources(resources.ModelResource):
    class Meta:
        model = CLASIFICACION_RESIDUOS


# Inclusión de el modelo REACTIVOS en la consola de administración de Django
@admin.register(CLASIFICACION_RESIDUOS)
class Reactivosadmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name','description', 'id','created_by','date_create','last_update','last_updated_by',)
    list_filter=('name','description',)
    search_fields=('name','description',)
    list_per_page=10
    ordering=('name',)
    resource_class = ClasificacionResources