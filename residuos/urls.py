#Archivo para definición de urls de las diferentes vistas o apis que interactuan el front con el back

from .views import *
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'residuos'

urlpatterns = [
    # UniCLab Residuos
    path('UniCLab_Residuos/', HomeUniCLabResiduos.as_view(), name='home_residuos'), # Página de incio del aplicativo residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Listado/', Wastes_Classification_List.as_view(), name='clasificacion_residuos'), # Página de incio del aplicativo residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Listado/Paginacion/<int:per_page>/', Wastes_Classification_Pagination.as_view(), name='Wastes_Classification_Pagination'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Autocompletar_Clasificaciones/', AutocompleteClassification.as_view(), name='autocomplete_class'), # Autocompletar en Usuarios
    path('UniCLab_Residuos/Clasificacion_Residuos/Listado/Exportar_a_Excel/', ExportToExcelClassification.as_view(), name='export_2_xls_classification'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Crear/', CrateWasteClassification.as_view(), name='create_classification'),# Crear Clasificación de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Editar/<str:pk>/', EditWasteClassification.as_view(), name='edit_classification'),# Editar Clasificación de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Desactivar/<str:pk>/', DisableWasteSorting.as_view(), name='disable_classification'), # Deshabilitar Clasificación
    path('UniCLab_Residuos/Clasificacion_Residuos/Activar/<str:pk>/', EnableWasteSorting.as_view(), name='enable_classification'), # Habilitar Clasificación
    path('UniCLab_Residuos/Registro_Residuos/Crear/', CreateRegisterWaste.as_view(), name='create_register'),# Crear Registro de residuos
    
    ]


