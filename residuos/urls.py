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
    path('UniCLab_Residuos/Clasificacion_Residuos/Listado/Pag/<int:per_page>/', Wastes_Classification_Pagination.as_view(), name='Wastes_Classification_Pagination'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Autocompletar_Clasificaciones/', AutocompleteClassification.as_view(), name='autocomplete_class'), # Autocompletar Clasificaciones
    path('UniCLab_Residuos/Clasificacion_Residuos/Listado/Exportar_a_Excel/', ExportToExcelClassification.as_view(), name='export_2_xls_classification'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Crear/', CrateWasteClassification.as_view(), name='create_classification'),# Crear Clasificación de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Editar/<str:pk>/', EditWasteClassification.as_view(), name='edit_classification'),# Editar Clasificación de residuos
    path('UniCLab_Residuos/Clasificacion_Residuos/Desactivar/<str:pk>/', DisableWasteSorting.as_view(), name='disable_classification'), # Deshabilitar Clasificación
    path('UniCLab_Residuos/Clasificacion_Residuos/Activar/<str:pk>/', EnableWasteSorting.as_view(), name='enable_classification'), # Habilitar Clasificación
    path('UniCLab_Residuos/Registro_Residuos/Crear/', CreateRegisterWaste.as_view(), name='create_register'),# Crear Registro de residuos
    path('UniCLab_Residuos/Registro_Residuos/Listado/', Wastes_Record_List.as_view(), name='record_waste_list'),# Listado Registro de residuos
    path('UniCLab_Residuos/Registro_Residuos/Listado/Pag/<int:per_page>/', Wastes_Record_Pagination.as_view(), name='Wastes_Record_Pagination'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Autocompletar_Residuos/', AutocompleteWaste.as_view(), name='autocomplete_waste'), # Autocompletar Residuos
    path('UniCLab_Residuos/Registro_Residuos/Listado/Exportar_a_Excel/', Export2ExcelWastes.as_view(), name='export_2_xls_wastes'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Registro_Residuos/Editar/<str:pk>/', EditarRegistroResiduos.as_view(), name='edit_register'),# Editar Registro de residuos
    path('UniCLab_Residuos/Registro_Residuos/Desactivar/<str:pk>/', DisableWasteRecord.as_view(), name='disable_record_waste'), # Deshabilitar Clasificación
    path('UniCLab_Residuos/Registro_Residuos/Activar/<str:pk>/', EnableWasteRecord.as_view(), name='enable_record_waste'), # Habilitar Registro
    
    ]


