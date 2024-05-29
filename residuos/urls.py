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
    path('UniCLab_Residuos/Registro_Residuos/Solicitud/', Temporal_Wastes_Record.as_view(), name='request_register'),# Vista para acumular registros antes de hacer la solicitud
    path('UniCLab_Residuos/Registro_Residuos/Enviar_Solicitud/', SendWasteRecord.as_view(), name='send_request_register'),# Enviar solicitud
    path('UniCLab_Residuos/Registro_Residuos/Cancelar_Solicitud/', CancelWasteRecord.as_view(), name='cancel_request_register'),# Cancelar solicitud
    path('UniCLab_Residuos/Registro_Residuos/Eliminar/<str:pk>/', DeleteWaste.as_view(), name='delete_record_waste'), # Eliminar residuo de la lista "Temporal"
    path('UniCLab_Residuos/Registro_Residuos/Listado/', Wastes_Record_List.as_view(), name='record_waste_list'),# Listado Registro de residuos
    path('UniCLab_Residuos/Registro_Residuos/Solicitudes/Ver/<str:pk>/', SolicitudPDFEmbView.as_view(), name='view_request_waste_html_emb'),# Ver solicitud en html
    path('UniCLab_Residuos/Registro_Residuos/Solicitudes/Borrar/', DeletePDFView.as_view(), name='delete_pdf'),# Borrar solicitud en pdf
    path('UniCLab_Residuos/Registro_Residuos/Eliminar_Registro/<str:pk>/', DeleteWasteRecordView.as_view(), name='delete_waste'), # Eliminar residuo de la lista principal
    path('UniCLab_Residuos/Registro_Residuos/No_leido/<str:pk>/', markAsUnread.as_view(), name='markasunread_record_waste'), # Marcar como no leída solicitud de residuo
    
    path('UniCLab_Residuos/Registro_Residuos/Listado/Pag/<int:per_page>/', Wastes_Record_Pagination.as_view(), name='Wastes_Record_Pagination'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Autocompletar_Residuos/', AutocompleteWaste.as_view(), name='autocomplete_waste'), # Autocompletar Residuos
    path('UniCLab_Residuos/Registro_Residuos/Listado/Exportar_a_Excel/', Export2ExcelWastes.as_view(), name='export_2_xls_wastes'),# Maneja paginación de listado de residuos
    path('UniCLab_Residuos/Registro_Residuos/Editar/<str:pk>/', EditarRegistroResiduos.as_view(), name='edit_register'),# Editar Registro de residuos
    path('UniCLab_Residuos/Registro_Residuos/Desactivar/<str:pk>/', DisableWasteRecord.as_view(), name='disable_record_waste'), # Deshabilitar Clasificación
    path('UniCLab_Residuos/Registro_Residuos/Activar/<str:pk>/', EnableWasteRecord.as_view(), name='enable_record_waste'), # Habilitar Registro
    path('UniCLab_Residuos/Usuarios/Cambiar_pass/', PasswordChangeView.as_view(), name='change_password'), # Cambiar contraseña
    path('UniCLab_Residuos/Cerrar_Sesion/', LogoutView.as_view(), name='logout'), # Cerrar Sesión
    path('UniCLab_Residuos/Solicitudes_Externas/Listado/', SolicitudesExtListView.as_view(), name='external_requests'), # Listado de solicitudes Externas
    path('UniCLab_Residuos/Solicitudes_Externas/Listado/Pag/<int:per_page>/', GuardarPerPageViewExternalRequests.as_view(), name='External_Request_Pagination'),# Maneja paginación de listado de solicitudes externas
    path('UniCLab_Residuos/Solicitudes_Externas/Enviar_Notificacion/', SendReadNotificationRequest.as_view(), name='send_read_notificacion_waste'),# Envía notificación de lectura a solicitud externa
    path('UniCLab_Residuos/Solicitudes/Registrar/', RegistrarSolicitudResiduos.as_view(), name='internal_requests_form'), # Listado de solicitudes Externas
    path('UniCLab_Residuos/Fichas_Seguridad/Crear/', CreateSecuritySheet.as_view(), name='security_sheet_create'), # Crear Fichas de seguirdad
    path('UniCLab_Residuos/Fichas_Seguridad/Ver/', Security_Sheet_List.as_view(), name='security_sheet_view'), # ver Fichas de seguirdad
    path('UniCLab_Residuos/Fichas_Seguridad/Editar/<str:pk>/', EditarSecuritySheet.as_view(), name='security_sheet_edit'), # editar Fichas de seguirdad
    path('UniCLab_Residuos/Fichas_Seguridad/Desactivar/<str:pk>/', DisableSecuritySheet.as_view(), name='security_sheet_disable'), # desactivar Fichas de seguirdad
    path('UniCLab_Residuos/Fichas_Seguridad/Activar/<str:pk>/', EnableSecuritySheet.as_view(), name='security_sheet_enable'), # activar Fichas de seguirdad
    path('UniCLab_Residuos/Certificados_Disposicion/Crear/', FinalCertificate.as_view(), name='final_certificate_create'), # Crear Certificado de disposición
    path('UniCLab_Residuos/Certificados_Disposicion/Ver/', FinalCertificateList.as_view(), name='final_certificate_view'), # Ver Certificado de disposición
    path('UniCLab_Residuos/Certificados_Disposicion/Ver/Pag/<int:per_page>/', FinalCertificateList_Pagination.as_view(), name='final_certificate_view_pagination'),# Maneja paginación de listado de certificaión
    path('UniCLab_Residuos/Certificados_Disposicion/Editar/<str:pk>/', EditFinalCertificate.as_view(), name='final_certificate_edit'),# Editar certificado de diposición final
    path('UniCLab_Residuos/Certificados_Disposicion/Deshabilitar/<str:pk>/', DisableFinalDispositionCertificate.as_view(), name='final_certificate_disable'),# Deshabilitar certificado de diposición final
    path('UniCLab_Residuos/Certificados_Disposicion/Habilitar/<str:pk>/', EnableFinalDispositionCertificate.as_view(), name='final_certificate_enable'),# Habilitar certificado de diposición final
    path('UniCLab_Residuos/Enlaces_Interes/Crear/', CreateImportantLinks.as_view(), name='important_link_create'),# Crear material de interés
    path('UniCLab_Residuos/Enlaces_Interes/Ver/', ViewImportantLinks.as_view(), name='important_link_view'),# Ver material de interés
    
    
    path('UniCLab_Residuos/Video/', ShowVideoView.as_view(), name='video'),# Habilitar certificado de diposición final

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


