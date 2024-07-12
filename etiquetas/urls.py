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
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


