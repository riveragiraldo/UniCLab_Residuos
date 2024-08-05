#Archivo para definición de urls de las diferentes vistas o apis que interactuan el front con el back

from .views import *
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'etiquetas'

urlpatterns = [
    # UniCLab Etiquetas
    path('UniCLab/Etiquetas/Generar_Etiquetas/', GenerateLabel.as_view(), name='generate_label'), # Página de incio del aplicativo etiquetas, generar etiquetas
    path('UniCLab/Etiquetas/Automcompletar_Sustancias/', autocompleteChemicalSubstances.as_view(), name='autocomplete_substances'), # Página de incio del aplicativo etiquetas, generar etiquetas
    path('UniCLab/Etiquetas/Formato_Etiquetas/', DownloadFormatLabelView.as_view(), name='download_format'), # Descargar formato en blanco
    path('UniCLab/Etiquetas/Etiqueta_Basica/', GenerateBasicLabel.as_view(), name='download_basic_label'), # Descargar etiqueta básica
    path('UniCLab/Etiquetas/Etiqueta_Pequena/', GenerateSmallLabel.as_view(), name='download_small_label'), # Descargar etiqueta pequeña
    path('UniCLab/Etiquetas/Etiqueta_Mediana/', GenerateMediumLabel.as_view(), name='download_medium_label'), # Descargar etiqueta mediana
    path('UniCLab/Etiquetas/Etiqueta_Grande/', GenerateBigLabel.as_view(), name='download_big_label'), # Descargar etiqueta grande
    path('UniCLab/Etiquetas/Listado_Pictogramas/', PictogramsList.as_view(), name='pictograms_list'), # Listado de Pictogramas
    path('UniCLab/Etiquetas/Cargar_Pictograma/', LoadNewPictogram.as_view(), name='load_new_pictogram'), # Cargar Nuevo Pictograma
    path('UniCLab/Etiquetas/Editar_Pictograma/<str:id>/', EditPictogram.as_view(), name='edit_pictogram'),  # Editar Pictograma
    path('UniCLab/Etiquetas/Inhabilitar_Pictograma/<str:id>/', DisablePictogram.as_view(), name='disable_pictogram'),  # Inhabilitar Pictograma
    path('UniCLab/Etiquetas/Habilitar_Pictograma/<str:id>/', EnablePictogram.as_view(), name='enable_pictogram'),  # Habilitar Pictograma
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


