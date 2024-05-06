from django.shortcuts import render
from reactivos.views import *
from .models import *
from reactivos.models import *
from django.views.generic import ListView, View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse, HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta, date
from django.utils.timezone import make_aware
from django.db.models import Q
from django.utils.http import urlencode
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect
import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as ExcelImage
from django.contrib.staticfiles import finders
from PIL import Image as PILImage
from django.utils.timezone import make_aware
from django.db.models import Q
from datetime import datetime
import os
from .forms import *
import base64
import pytz
from django.db.models import F, ExpressionWrapper, DecimalField




# ---------------------------------------------------------- #
# Función para validar usuarios con acceso
def check_group_permission(groups_required):
    def decorator(view_func):
        @method_decorator(login_required)
        def _wrapped_view(self, request, *args, **kwargs):
            grupos_usuario = self.request.user.groups.all().values('name')
            is_of_group = False
            
            for grupo in grupos_usuario:
                for grupo_requerido in groups_required:
                    if grupo['name'] == grupo_requerido:
                        is_of_group = True
                        break
            
            if is_of_group or self.request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            else:
                messages.error(request, 'No tiene permisos para acceder a esta vista, desea acceder con credenciales distintas')
                return HttpResponseRedirect(reverse('reactivos:login'))

        return _wrapped_view
    return decorator



# ---------------------------------------------------------- #
# Vista para la creación página principal de aplicativo de residuos,
class HomeUniCLabResiduos(View):  # Utiliza LoginRequiredMixin como clase base
    template_name = 'UniCLab_Residuos/index.html'  # Nombre de la plantilla

    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request,*args,**kwargs):
        
             
        context = {
            
        }
        return render(request, self.template_name, context)


# ---------------------------------------------------------- #
# Listado de Clasificación de residuos
class Wastes_Classification_List(LoginRequiredMixin,ListView):
    model = CLASIFICACION_RESIDUOS
    template_name = "UniCLab_Residuos/listado_clasificaciones.html"
    paginate_by = 10
    
    
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Obtener el número de registros por página de la sesión del usuario
        per_page = request.session.get('per_page')
        if per_page:
            self.paginate_by = int(per_page)
        else:
            self.paginate_by = 10  # Valor predeterminado si no hay variable de sesión

        # Obtener los parámetros de filtrado
        
        # Obtener las fechas de inicio y fin de la solicitud GET
        name = self.request.GET.get('name')
        id_classification = self.request.GET.get('id_classification')
           
        # Guardar los valores de filtrado en la sesión
        
        request.session['filtered_name'] = name
        request.session['filtered_id_classification'] = id_classification
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['usuarios'] = User.objects.all()
        context['laboratorios'] = Laboratorios.objects.all()
        
       
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()

        id_classification = self.request.GET.get('id_classification')
        if id_classification:
            queryset = queryset.filter(id=id_classification)

        queryset = queryset.order_by('id')
        return queryset
    
# ------------------------------------------------ #
# Paginación de listado de clasifición de residuos #
class Wastes_Classification_Pagination(LoginRequiredMixin,View):
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        per_page = kwargs.get('per_page')
        request.session['per_page'] = per_page

        # Redirigir a la página de inventario con los parámetros de filtrado actuales
        
        filtered_name = request.session.get('filtered_name')
        filtered_id_classification = request.session.get('filtered_id_classification')
        
        url = reverse('residuos:clasificacion_residuos')
        params = {}
        
        if filtered_name:
            params['name'] = filtered_name
        if filtered_id_classification:
            params['id_classification'] = filtered_id_classification
                
        
        if params:
            url += '?' + urlencode(params)

        return redirect(url)


# --------------------------------- #
# Autocompletado de clasificaciones #

class AutocompleteClassification(LoginRequiredMixin,View):
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request):
        term = request.GET.get('term', '')
        
        clasificaciones = CLASIFICACION_RESIDUOS.objects.filter(
                Q(name__icontains=term) | Q(description__icontains=term)).order_by('description')[:20]
        

        results = []
        for clasificacion in clasificaciones:
            result = {
                'name': clasificacion.name,
                'description': clasificacion.description,
                'id_classification':clasificacion.id,
            }
            results.append(result)
        return JsonResponse(results, safe=False)
    
# ------------------------------------------------------- #
# Exportar a Excel listado de Clasiifcaciones de residuos #

class ExportToExcelClassification(LoginRequiredMixin, View):
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    

    
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        def get_file_name():
            now = datetime.now()
            return f'Clasificacion_residuos_decreto_1076_2015_{now.strftime("%d%m%Y%H%M%S")}.xlsx'
        id_classification = request.session.get('filtered_id_classification')
        queryset=CLASIFICACION_RESIDUOS.objects.all()
        if id_classification:
            queryset = queryset.filter(id=id_classification)

        queryset = queryset.order_by('id')

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        logo_path = finders.find('inventarioreac/Images/escudoUnal_black.png')
        pil_image = PILImage.open(logo_path)
        image = ExcelImage(pil_image)
        sheet.add_image(image, 'A1')

        fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        sheet['B1'] = 'Clasificación de residuos según decreto 2076 de 2015'
        sheet['B2'] = 'Fecha de Creación: '+fecha_creacion
        sheet['A4'] = 'Nombre'
        sheet['B4'] = 'Descripción'
        sheet['C4'] = 'Estado'

        sheet.row_dimensions[1].height = 30
        sheet.row_dimensions[2].height = 30
        sheet.row_dimensions[3].height = 25

        Titulo = sheet['B1']
        Titulo.font = Font(bold=True, size=16)
        Titulo.alignment = Alignment(horizontal='right')

        Fecha = sheet['B2']
        Fecha.alignment = Alignment(horizontal='right')
        
        

        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        bold_font = Font(bold=True)

        sheet.column_dimensions['A'].width = 10
        sheet.column_dimensions['B'].width = 125

        alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
        

        row = 4
        for col in range(1, 4):
            sheet.cell(row=row, column=col).border = thin_border
            sheet.cell(row=row, column=col).font = bold_font

        row = 5
        for item in queryset:
            if item.is_active:
                Estado="Activo"
            else:
                Estado="Inactivo"
            sheet.cell(row=row, column=1).value = (item.name)
            sheet.cell(row=row, column=2).value = (item.description)
            sheet.cell(row=row, column=3).value = Estado
            

            for col in range(1, 4):
                sheet.cell(row=row, column=col).border = thin_border
                sheet.cell(row=row, column=col).alignment = alignment

            row += 1

        start_column = 1
        end_column = 3
        start_row = 4
        end_row = row - 1

        start_column_letter = get_column_letter(start_column)
        end_column_letter = get_column_letter(end_column)

        table_range = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"

        sheet.auto_filter.ref = table_range

        fill = PatternFill(fill_type="solid", fgColor=WHITE)
        start_cell = sheet['A1']
        end_column_letter = get_column_letter(end_column+1)
        end_row = row+1
        end_cell = sheet[end_column_letter + str(end_row)]
        table_range = start_cell.coordinate + ':' + end_cell.coordinate

        for row in sheet[table_range]:
            for cell in row:
                cell.fill = fill

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={get_file_name()}'

        workbook.save(response)

        tipo_evento = 'DESCARGA DE ARCHIVOS'
        usuario_evento = request.user
        crear_evento(tipo_evento, usuario_evento)

        return response
    
# ------------------------------- #
# Crear Clasificación de Residuos #

class CrateWasteClassification(LoginRequiredMixin ,View):
    template_name = 'UniCLab_Residuos/crear_clasificacion.html'

    
    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        form = ClasificacionResiduosForm()
        return render(request, self.template_name, {'form': form})
    
    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def post(self, request, *args, **kwargs):
        form = ClasificacionResiduosForm(request.POST, request.FILES)
        
        try:
            if form.is_valid():
                # Asignar el usuario actual a los campos created_by y last_updated_by
                form.instance.created_by = request.user
                form.instance.last_updated_by = request.user
                # Guardar la clasificación si el formulario es válido
                clasificacion = form.save()
                
                # Registrar evento
                tipo_evento = 'CREAR CLASIFICACION DE RESIDUOS'
                usuario_evento = request.user
                crear_evento(tipo_evento, usuario_evento)
                
                mensaje=f'Clasificación de residuos creada correctamente.'
                # Devuelve una respuesta JSON de éxito
                return JsonResponse({'success': True, 'message': mensaje})
                
                
            else:
                # Devuelve una respuesta JSON con los errores de validación
                return JsonResponse({'success': False, 'errors': form.errors})
            
        except Exception as e:
            # Imprimir el error en la consola o logs
            print(e)
            mensaje=f'Error: {e}'
            # Devolver una respuesta de error o redirigir a una página de error
            return HttpResponseBadRequest(f'Error interno del servidor:{mensaje}')
   
# -------------------------------- #
# Editar Clasificación de Residuos #

class EditWasteClassification(LoginRequiredMixin, View):
    template_name = 'UniCLab_Residuos/editar_clasificacion.html'

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        try:
            # Decodificar el ID en base64 dos veces
            class_key = kwargs.get('pk')
            classification_id = base64.urlsafe_b64decode(base64.urlsafe_b64decode(class_key)).decode('utf-8')
            
            # Obtener la clasificación de residuos que se va a editar
            clasificacion = get_object_or_404(CLASIFICACION_RESIDUOS, id=classification_id)
            
            # Crear el formulario con los datos de la clasificación
            form = ClasificacionResiduosForm(instance=clasificacion)
            return render(request, self.template_name, {'form': form, 'clasificacion': clasificacion})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error interno del servidor')

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def post(self, request, *args, **kwargs):
        try:
            # Decodificar el ID en base64 dos veces
            class_key = kwargs.get('pk')
            classification_id = base64.urlsafe_b64decode(base64.urlsafe_b64decode(class_key)).decode('utf-8')
            
            # Obtener la clasificación de residuos que se va a editar
            clasificacion = get_object_or_404(CLASIFICACION_RESIDUOS, id=classification_id)
            
            form = ClasificacionResiduosForm(request.POST, request.FILES, instance=clasificacion)
            if form.is_valid():
                # Asignar el usuario actual a last_updated_by
                form.instance.last_updated_by = request.user
                # Guardar los cambios si el formulario es válido
                clasificacion = form.save()

                # Registrar evento
                tipo_evento = 'EDICION CLASIFICACION DE RESIDUOS'
                usuario_evento = request.user
                crear_evento(tipo_evento, usuario_evento)

                mensaje = 'Clasificación de residuos actualizada correctamente.'
                return JsonResponse({'success': True, 'message': mensaje})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print(e)
            mensaje = f'Error: {e}'
            return HttpResponseBadRequest(f'Error interno del servidor:{mensaje}')

# ------------------------------------ #
# Desactivar Clasificación de Residuos #

class DisableWasteSorting(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el ID codificado dos veces desde los parámetros de la solicitud
            class_key = kwargs.get('pk')
            item_id_encoded = base64.urlsafe_b64decode(class_key).decode('utf-8')
            classification_id = base64.urlsafe_b64decode(item_id_encoded).decode('utf-8')
            
            # Obtener la instancia de la clasificación de residuos
            clasificacion = get_object_or_404(CLASIFICACION_RESIDUOS, id=classification_id)
            # incluir el usuario que realiza el cambio
            clasificacion.last_updated_by= request.user
            # Desactivar la clasificación de residuos
            clasificacion.is_active = False
            clasificacion.save()
            
            # Registrar evento
            tipo_evento = 'DESACTIVAR CLASIFICACION DE RESIDUOS'
            usuario_evento = request.user
            crear_evento(tipo_evento, usuario_evento)

            # Devolver una respuesta JSON de éxito
            return JsonResponse({'success': True, 'message': f'Clasificación "{clasificacion.name}" desactivada correctamente.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Error interno del servidor'})
        
# --------------------------------- #
# Activar Clasificación de Residuos #

class EnableWasteSorting(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el ID codificado dos veces desde los parámetros de la solicitud
            class_key = kwargs.get('pk')
            item_id_encoded = base64.urlsafe_b64decode(class_key).decode('utf-8')
            classification_id = base64.urlsafe_b64decode(item_id_encoded).decode('utf-8')
            
            # Obtener la instancia de la clasificación de residuos
            clasificacion = get_object_or_404(CLASIFICACION_RESIDUOS, id=classification_id)
            # incluir el usuario que realiza el cambio
            clasificacion.last_updated_by= request.user
            # Desactivar la clasificación de residuos
            clasificacion.is_active = True
            clasificacion.save()

            # Registrar evento
            tipo_evento = 'ACTIVAR CLASIFICACION DE RESIDUOS'
            usuario_evento = request.user
            crear_evento(tipo_evento, usuario_evento)
            
            # Devolver una respuesta JSON de éxito
            return JsonResponse({'success': True, 'message': f'Clasificación "{clasificacion.name}" activada correctamente.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Error interno del servidor'})
        
# -------------------------- #
# Crear Registro de Residuos #

class CreateRegisterWaste(LoginRequiredMixin, View):
    template_name = 'UniCLab_Residuos/crear_registro_residuos.html'

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL', 'COORDINADOR', 'TECNICO'])
    def get(self, request, *args, **kwargs):
        form = RegistroResiduosForm()
        laboratorios=Laboratorios.objects.all()
        lab_id=request.user.lab.id

        return render(request, self.template_name, {'form': form, 'laboratorios':laboratorios, 'lab_id':lab_id})

    def enviar_correo_asincrono(self, recipient_list, subject, message, attach_path):
        try:
            enviar_correo(recipient_list, subject, message, attach_path)
        except Exception as e:
            print(f'Error al enviar correo: {e}')

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL', 'COORDINADOR', 'TECNICO'])
    def post(self, request, *args, **kwargs):
        form = RegistroResiduosForm(request.POST)
        try:
            if form.is_valid():
                # Asignar el usuario actual a los campos created_by y last_updated_by
                form.instance.created_by = request.user
                form.instance.last_updated_by = request.user
                # Guardar el registro si el formulario es válido
                registro_residuo = form.save()
                registro_residuo.total_residuo=registro_residuo.cantidad*registro_residuo.numero_envases
                registro_residuo.save()
                
                # Registrar evento
                tipo_evento = 'CREAR REGISTRO DE RESIDUOS'
                usuario_evento = request.user
                crear_evento(tipo_evento, usuario_evento)

                # Datos para correo electrónico

                # Usuarios que recepcionan
                # Obtener el correo del usuario que realiza el registro
                correo_usuario = request.user.email

                # Obtener los correos de todos los usuarios activos con rol 'ADMINISTRADOR AMBIENTAL'
                usuarios_admin_ambiental = User.objects.filter(is_active=True, rol__name='ADMINISTRADOR AMBIENTAL').values_list('email', flat=True)

                # Crear una lista de destinatarios
                recipient_list = list(usuarios_admin_ambiental)
                recipient_list.append(correo_usuario)  # Agregar el correo del usuario que realiza el registro

                # Asunto
                subject= f'Registro exitoso de residuo {registro_residuo.nombre_residuo}'

                # Mensaje
                # Definir como dependencia el area o laboratorio
                if registro_residuo.area and registro_residuo.laboratorio:
                    dependencia=f'{registro_residuo.area} {registro_residuo.laboratorio.name}'
                elif registro_residuo.area:
                    dependencia=f'{registro_residuo.area}'
                elif registro_residuo.laboratorio:
                    dependencia=f'{registro_residuo.laboratorio.name}'
                
                # sacar el total del residuo del registro
                total_residuo=registro_residuo.numero_envases*registro_residuo.cantidad

                # Organizar las clasificaciones
                clasificaciones = ', '.join(registro_residuo.clasificado.values_list('name', flat=True)) if registro_residuo.clasificado.exists() else 'NO DEFINIDA'
                
                # Formatear fecha    
                # Obtener el huso horario deseado (GMT-5)
                tz = pytz.timezone('America/Bogota')

                # Convertir la fecha al huso horario deseado y formatearla
                fecha_registro = registro_residuo.date_create.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
    

                header=f'<p>El siguiente mensaje tiene el fin de informarte que recientemente se ha realizado un registro de residuos dirgido a la <i>OFICINA AMBIENTAL</i> de la Universidad Nacional de Colombia, los datos del registro son los siguientes:</p>'
                body=f'<p><b>Fecha del registro: </b>{fecha_registro}<br><b>Consecutivo: </b>{registro_residuo.pk}<br><b>Dependencia: </b>{dependencia}<br><b>Nombre del residuo: </b>{registro_residuo.nombre_residuo}<br><b>Cantidad: </b>{registro_residuo.cantidad} {registro_residuo.unidades.name}<br><b>Cantidad de envases: </b>{registro_residuo.numero_envases}<br><b>Total residuo: </b>{total_residuo} {registro_residuo.unidades.name}<br><b>Clasificación Y - A: </b>{clasificaciones}<br><b>Estado: </b>{registro_residuo.estado.name}<br><b>Responsable del registro: </b>{registro_residuo.created_by.first_name} {registro_residuo.created_by.last_name}<br><b>Correo electrónio: </b>{registro_residuo.created_by.email}<br><b>Observaciones: </b>{registro_residuo.observaciones}</p>'
                footer=f'<p>Este correo es informativo, para más detalle dirigite a la web principal de UniCLab Residuos.</p>'
                message=header+body+footer
                
                # Adjuntos
                attach_path=None
               
                
                # Crear un hilo y ejecutar enviar_correo en segundo plano
                correo_thread = threading.Thread(
                    target=self.enviar_correo_asincrono,
                    args=(recipient_list, subject, message, attach_path),
                )
                correo_thread.start()

                
                mensaje = 'Registro de residuo creado correctamente.'
                return JsonResponse({'success': True, 'message': mensaje})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print(e)
            mensaje = f'Error: {e}'
            return HttpResponseBadRequest(f'Error interno del servidor: {mensaje}')
        
# ------------------------------------------- #
# Listado de Registro de residups de residuos #
class Wastes_Record_List(LoginRequiredMixin,ListView):
    model = REGISTRO_RESIDUOS
    template_name = "UniCLab_Residuos/listado_registros_residuos.html"
    paginate_by = 10
    
    
    @check_group_permission(groups_required=['ADMINISTRADOR','ADMINISTRADOR AMBIENTAL','COORDINADOR','TECNICO'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Obtener el número de registros por página de la sesión del usuario
        per_page = request.session.get('per_page')
        if per_page:
            self.paginate_by = int(per_page)
        else:
            self.paginate_by = 10  # Valor predeterminado si no hay variable de sesión

        # Obtener los parámetros de filtrado
        
        # Obtener las fechas de inicio y fin de la solicitud GET
        id_laboratorio = self.request.GET.get('id_laboratorio')
        name = self.request.GET.get('name')
        start_date = self.request.GET.get('start_date')   
        end_date = self.request.GET.get('end_date')   
        # Guardar los valores de filtrado en la sesión
        
        request.session['filtered_id_laboratorio'] = id_laboratorio
        request.session['filtered_name'] = name
        request.session['filtered_start_date'] = start_date
        request.session['filtered_end_date'] = end_date
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # Otros datos que quieras pasar al contexto
        context['usuarios'] = User.objects.all()
        context['laboratorios'] = Laboratorios.objects.all()
        # Obtener la fecha de hoy
        today = timezone.now().date()

        # Pasar la fecha de hoy al contexto
        context['today'] = today

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()

        id_laboratorio = self.request.GET.get('id_laboratorio')

        name = self.request.GET.get('name')
        
        # Obtener las fechas de inicio y fin de la solicitud GET
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Validar y convertir las fechas
        try:
            if start_date:
                start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
        except ValueError:
            # Manejar errores de formato de fecha aquí si es necesario
            pass

        
        # Realiza la filtración de acuerdo a las fechas
        if start_date:
            queryset = queryset.filter(date_create__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_create__lte=end_date)
        elif start_date and end_date:
            queryset = queryset.filter(date_create__gte=start_date,date_create__lte=end_date)


        # Filtrar por  campos que contengan la palabra clave en su nombre
        if name:
            queryset = queryset.filter(Q(nombre_residuo__icontains=name) | Q(area__icontains=name) | Q(laboratorio__name__icontains=name) | Q(clasificado__name__icontains=name))
        

        if id_laboratorio:
            queryset = queryset.filter(laboratorio=id_laboratorio)

        queryset = queryset.order_by('id')
        return queryset
    
# --------------------------------------------- #
# Paginación de listado de registro de residuos #
class Wastes_Record_Pagination(LoginRequiredMixin,View):
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        per_page = kwargs.get('per_page')
        request.session['per_page'] = per_page

        # Redirigir a la página de inventario con los parámetros de filtrado actuales
        filtered_id_laboratorio = request.session.get('filtered_id_laboratorio')
        filtered_name = request.session.get('filtered_name')
        filtered_start_date = request.session.get('filtered_start_date')
        filtered_end_date = request.session.get('filtered_end_date')
        
        url = reverse('residuos:record_waste_list')
        params = {}
        
        if filtered_id_laboratorio:
            params['id_laboratorio'] = filtered_id_laboratorio
        if filtered_name:
            params['name'] = filtered_name
        if filtered_start_date:
            params['start_date'] = filtered_start_date
        if filtered_end_date:
            params['end_date'] = filtered_end_date
        
        if params:
            url += '?' + urlencode(params)

        return redirect(url)

    
# --------------------------------- #
# Autocompletar listado de residuos #
class AutocompleteWaste(LoginRequiredMixin, View):
    @check_group_permission(groups_required=['ADMINISTRADOR', 'COORDINADOR', 'TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request):
        term = request.GET.get('term', '')

        # Filtrar los residuos y obtener valores únicos
        residuos = REGISTRO_RESIDUOS.objects.filter(
            nombre_residuo__icontains=term
        ).values('nombre_residuo').distinct()[:10]

        # Convertir a mayúsculas y obtener valores únicos
        nombres_mayuscula = set(residuo['nombre_residuo'].upper() for residuo in residuos)

        # Crear una lista de resultados
        results = [{'name': nombre} for nombre in nombres_mayuscula]

        return JsonResponse(results, safe=False)
    
# ------------------------------------- #
# Exportar a Excel registro de residuos #
class Export2ExcelWastes(LoginRequiredMixin, View):
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
       
    @check_group_permission(groups_required=['ADMINISTRADOR','COORDINADOR','TECNICO', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        def get_file_name():
            now = datetime.now()
            return f'Registro_de_residuos_{now.strftime("%d%m%Y%H%M%S")}.xlsx'
           
        queryset=REGISTRO_RESIDUOS.objects.all()
        
        # Obtener datos filtrados de la sesión
        id_laboratorio = request.session.get('filtered_id_laboratorio')
        name = request.session.get('filtered_name')
        start_date = request.session.get('filtered_start_date')
        end_date = request.session.get('filtered_end_date')
        
        # Validar y convertir las fechas
        try:
            if start_date:
                start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
        except ValueError:
            # Manejar errores de formato de fecha aquí si es necesario
            pass

        
        # Realiza la filtración de acuerdo a las fechas
        if start_date:
            queryset = queryset.filter(date_create__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_create__lte=end_date)
        elif start_date and end_date:
            queryset = queryset.filter(date_create__gte=start_date,date_create__lte=end_date)


        # Filtrar por  campos que contengan la palabra clave en su nombre
        if name:
            queryset = queryset.filter(Q(nombre_residuo__icontains=name) | Q(area__icontains=name) | Q(laboratorio__name__icontains=name) | Q(clasificado__name__icontains=name))
        

        if id_laboratorio:
            queryset = queryset.filter(laboratorio=id_laboratorio)

        queryset = queryset.order_by('id')

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        logo_path = finders.find('inventarioreac/Images/escudoUnal_black.png')
        pil_image = PILImage.open(logo_path)
        image = ExcelImage(pil_image)
        sheet.add_image(image, 'A1')

        fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        sheet['C1'] = 'Listado de registro de residuos'
        sheet['C2'] = 'Fecha de Creación: '+fecha_creacion
        sheet['A4'] = 'Consecutivo'
        sheet['B4'] = 'Dependencia'
        sheet['C4'] = 'Nombre del residuo'
        sheet['D4'] = 'Cantidad'
        sheet['E4'] = 'Número de envases'
        sheet['F4'] = 'Total Residuo'
        sheet['G4'] = 'Unidades'
        sheet['H4'] = 'Clasificado Y - A'
        sheet['I4'] = 'Estado'
        sheet['J4'] = 'Dependencia que realiza registro'
        sheet['K4'] = 'Usuario que registra'
        sheet['L4'] = 'Registro Activo?'

        sheet.row_dimensions[1].height = 30
        sheet.row_dimensions[2].height = 30
        sheet.row_dimensions[3].height = 25

        Titulo = sheet['C1']
        Titulo.font = Font(bold=True, size=16)
        Titulo.alignment = Alignment(horizontal='left')

        Fecha = sheet['C2']
        Fecha.alignment = Alignment(horizontal='left')
        
        

        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        bold_font = Font(bold=True)

        # Establecer Anchos personalizados
        sheet.column_dimensions['A'].width = 12
        sheet.column_dimensions['B'].width = 31
        sheet.column_dimensions['C'].width = 27
        sheet.column_dimensions['D'].width = 10
        sheet.column_dimensions['E'].width = 10
        sheet.column_dimensions['F'].width = 10
        sheet.column_dimensions['G'].width = 10
        sheet.column_dimensions['H'].width = 10
        sheet.column_dimensions['I'].width = 10
        sheet.column_dimensions['J'].width = 21
        sheet.column_dimensions['K'].width = 31
        sheet.column_dimensions['L'].width = 10

        alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
        

        row = 4
        for col in range(1, 13):
            sheet.cell(row=row, column=col).border = thin_border
            sheet.cell(row=row, column=col).font = bold_font
            sheet.cell(row=row, column=col).alignment = alignment

        row = 5
        for item in queryset:
            # Crear la dependencia

            if item.laboratorio and item.area:
                dependencia=f'{item.laboratorio.name} {item.area}'
            elif item.laboratorio:
                dependencia=f'{item.laboratorio.name}'
            elif item.area:
                dependencia=f'{item.area}'
            
            # Organizar las clasificaciones
            clasificaciones = ', '.join(item.clasificado.values_list('name', flat=True)) if item.clasificado.exists() else 'NO DEFINIDA'

            # Definir el estado de activación
            if item.is_active:
                estado="SÍ"
            else:
                estado="NO"
            sheet.cell(row=row, column=1).value = (item.id)
            sheet.cell(row=row, column=2).value = (dependencia)
            sheet.cell(row=row, column=3).value = item.nombre_residuo
            sheet.cell(row=row, column=4).value = item.cantidad
            sheet.cell(row=row, column=5).value = item.numero_envases
            sheet.cell(row=row, column=6).value = item.total_residuo
            sheet.cell(row=row, column=7).value = item.unidades.name
            sheet.cell(row=row, column=8).value = clasificaciones
            sheet.cell(row=row, column=9).value = item.estado.name
            sheet.cell(row=row, column=10).value =item.created_by.lab.name
            sheet.cell(row=row, column=11).value = f'{item.created_by.first_name} {item.created_by.last_name}'
            sheet.cell(row=row, column=12).value = estado       
            
            for col in range(1, 13):
                sheet.cell(row=row, column=col).border = thin_border
                sheet.cell(row=row, column=col).alignment = alignment

            row += 1

        start_column = 1
        end_column = 12
        start_row = 4
        end_row = row - 1

        start_column_letter = get_column_letter(start_column)
        end_column_letter = get_column_letter(end_column)

        table_range = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"

        sheet.auto_filter.ref = table_range

        fill = PatternFill(fill_type="solid", fgColor=WHITE)
        start_cell = sheet['A1']
        end_column_letter = get_column_letter(end_column+1)
        end_row = row+1
        end_cell = sheet[end_column_letter + str(end_row)]
        table_range = start_cell.coordinate + ':' + end_cell.coordinate

        for row in sheet[table_range]:
            for cell in row:
                cell.fill = fill

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={get_file_name()}'

        workbook.save(response)

        tipo_evento = 'DESCARGA DE ARCHIVOS'
        usuario_evento = request.user
        crear_evento(tipo_evento, usuario_evento)

        return response
    
# ----------------------------------------- #
# Editar Registro de Residuos #
class EditarRegistroResiduos(LoginRequiredMixin, View):
    template_name = 'UniCLab_Residuos/editar_registro_residuos.html'

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def get(self, request, *args, **kwargs):
        try:
            # Decodificar el ID en base64 dos veces
            registro_key = kwargs.get('pk')
            registro_id = base64.urlsafe_b64decode(base64.urlsafe_b64decode(registro_key)).decode('utf-8')
            
            # Obtener el registro de residuos que se va a editar
            registro_residuo = get_object_or_404(REGISTRO_RESIDUOS, id=registro_id)
            
            # Crear el formulario con los datos del registro
            form = RegistroResiduosForm(instance=registro_residuo)
            laboratorios = Laboratorios.objects.all()
            lab_id = request.user.lab.id

            return render(request, self.template_name, {'form': form, 'laboratorios': laboratorios, 'lab_id': lab_id,'residuo': registro_residuo,})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error interno del servidor')

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def post(self, request, *args, **kwargs):
        try:
            # Decodificar el ID en base64 dos veces
            registro_key = kwargs.get('pk')
            registro_id = base64.urlsafe_b64decode(base64.urlsafe_b64decode(registro_key)).decode('utf-8')
            
            # Obtener el registro de residuos que se va a editar
            registro_residuo = get_object_or_404(REGISTRO_RESIDUOS, id=registro_id)
            
            form = RegistroResiduosForm(request.POST, request.FILES, instance=registro_residuo)
            if form.is_valid():
                # Asignar el usuario actual a last_updated_by
                form.instance.last_updated_by = request.user
                # Totalizar el residuo
                registro_residuo.total_residuo=registro_residuo.cantidad*registro_residuo.numero_envases
                # Guardar los cambios si el formulario es válido
                registro_residuo = form.save()

                # Registrar evento
                tipo_evento = 'EDICION REGISTRO DE RESIDUOS'
                usuario_evento = request.user
                crear_evento(tipo_evento, usuario_evento)

                mensaje = 'Registro de residuos actualizado correctamente.'
                return JsonResponse({'success': True, 'message': mensaje})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print(e)
            mensaje = f'Error: {e}'
            return HttpResponseBadRequest(f'Error interno del servidor:{mensaje}')


# ------------------------------------ #
# Desactivar Clasificación de Residuos #

class DisableWasteRecord(View):
    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el ID codificado dos veces desde los parámetros de la solicitud
            waste_key = kwargs.get('pk')
            item_id_encoded = base64.urlsafe_b64decode(waste_key).decode('utf-8')
            waste_record_id = base64.urlsafe_b64decode(item_id_encoded).decode('utf-8')
            
            # Obtener la instancia de la clasificación de residuos
            wate_record = get_object_or_404(REGISTRO_RESIDUOS, id=waste_record_id)
            # incluir el usuario que realiza el cambio
            wate_record.last_updated_by= request.user
            # Desactivar la clasificación de residuos
            wate_record.is_active = False
            wate_record.save()
            
            # Registrar evento
            tipo_evento = 'DESACTIVAR REGISTRO DE RESIDUOS'
            usuario_evento = request.user
            crear_evento(tipo_evento, usuario_evento)

            # Devolver una respuesta JSON de éxito
            return JsonResponse({'success': True, 'message': f'Registro de residuo"{wate_record.nombre_residuo}" deshabilitado correctamente.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Error interno del servidor'})
        
# --------------------------------- #
# Activar Clasificación de Residuos #

class EnableWasteRecord(View):
    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el ID codificado dos veces desde los parámetros de la solicitud
            waste_key = kwargs.get('pk')
            item_id_encoded = base64.urlsafe_b64decode(waste_key).decode('utf-8')
            waste_record_id = base64.urlsafe_b64decode(item_id_encoded).decode('utf-8')
            
            # Obtener la instancia de la clasificación de residuos
            wate_record = get_object_or_404(REGISTRO_RESIDUOS, id=waste_record_id)
            # incluir el usuario que realiza el cambio
            wate_record.last_updated_by= request.user
            # Desactivar la clasificación de residuos
            wate_record.is_active = True
            wate_record.save()
            
            # Registrar evento
            tipo_evento = 'ACTIVAR REGISTRO DE RESIDUOS'
            usuario_evento = request.user
            crear_evento(tipo_evento, usuario_evento)

            # Devolver una respuesta JSON de éxito
            return JsonResponse({'success': True, 'message': f'Registro de residuo"{wate_record.nombre_residuo}" habilitado correctamente.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Error interno del servidor'})
        
# ----------------------------- #        
# Vista para cambiar contraseña #        
class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("residuos:home_residuos")
    template_name = "UniCLab_Residuos/cambiar_pass.html"
    title = ("Password change")

    @check_group_permission(groups_required=['ADMINISTRADOR', 'ADMINISTRADOR AMBIENTAL'])
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        tipo_evento = 'CAMBIAR CONTRASENA'
        usuario_evento = self.request.user
        crear_evento(tipo_evento, usuario_evento)

        update_session_auth_hash(self.request, form.user)

        # Agregar un mensaje de éxito
        messages.success(self.request, 'Contraseña cambiada exitosamente.')

        return super().form_valid(form)

# ------------- #
# Cerrar Sesión #
class LogoutView(RedirectURLMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """

    # RemovedInDjango50Warning: when the deprecation ends, remove "get" and
    # "head" from http_method_names.
    http_method_names = ["get", "head", "post", "options"]
    template_name = "UniCLab_Residuos/logged_out_residuos.html"
    extra_context = None

    # RemovedInDjango50Warning: when the deprecation ends, move
    # @method_decorator(csrf_protect) from post() to dispatch().
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Crea un evento de cierre de sesión
            tipo_evento = 'CIERRE DE SESION'
            usuario_evento = self.request.user
            crear_evento(tipo_evento, usuario_evento)

        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    # RemovedInDjango50Warning.
    get = post

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                "site": current_site,
                "site_name": current_site.name,
                "title": ("Logged out"),
                "subtitle": None,
                **(self.extra_context or {}),
            }
        )
        return context
    
    def logout_then_login(request, login_url=None):
            """
            Log out the user if they are logged in. Then redirect to the login page.
            """
            login_url = resolve_url(login_url or settings.LOGIN_URL)
            return LogoutView.as_view(next_page=login_url)(request)
        
    def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
            """
            Redirect the user to the login page, passing the given 'next' page.
            """
            resolved_url = resolve_url(login_url or settings.LOGIN_URL)
    
            login_url_parts = list(urlparse(resolved_url))
            if redirect_field_name:
                querystring = QueryDict(login_url_parts[4], mutable=True)
                querystring[redirect_field_name] = next
                login_url_parts[4] = querystring.urlencode(safe="/")
    
            return HttpResponseRedirect(urlunparse(login_url_parts))
    
# ------------------------------- #
# Listado de solicitudes Externas #
class SolicitudesExtListView(LoginRequiredMixin,ListView):
    model = SolicitudesExternas
    template_name = "UniCLab_Residuos/listado_solicitudes_externas.html"
    paginate_by = 10
    
    
    @check_group_permission(groups_required=['ADMINISTRADOR','ADMINISTRADOR AMBIENTAL'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Obtener el número de registros por página de la sesión del usuario
        per_page = request.session.get('per_page')
        if per_page:
            self.paginate_by = int(per_page)
        else:
            self.paginate_by = 10  # Valor predeterminado si no hay variable de sesión

        # Obtener los parámetros de filtrado
        
        # Obtener las fechas de inicio y fin de la solicitud GET
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        lab = self.request.GET.get('lab')
        keyword = self.request.GET.get('keyword')  
        
        

        # Guardar los valores de filtrado en la sesión
        
        request.session['filtered_start_date'] = start_date
        request.session['filtered_end_date'] = end_date
        request.session['filtered_lab'] = lab
        request.session['filtered_keyword'] = keyword
        

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la fecha de hoy
        today = date.today()
        # Calcular la fecha hace un mes hacia atrás
        one_month_ago = today - timedelta(days=30)

        # Agregar la fecha al contexto
        context['one_month_ago'] = one_month_ago

        # Agregar la fecha de hoy al contexto
        context['today'] = today
        laboratorio = self.request.user.lab
        
    
        context['usuarios'] = User.objects.all()
        context['laboratorio'] = laboratorio
        context['laboratorios'] = Laboratorios.objects.all()
        
        # Obtener la lista de inventarios
        entradas = context['object_list']
        # Recorrer los entradas y cambiar el formato de la fecha        
               
        context['object_list'] = entradas
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()

        lab = self.request.GET.get('lab')
        keyword = self.request.GET.get('keyword')
        
        

        # si el valor de lab viene de sesión superusuario o ADMINISTRADOR lab=0 cambiar por lab=''
        if lab=='0':
             lab=''

        # Obtener las fechas de inicio y fin de la solicitud GET
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Validar y convertir las fechas
        try:
            if start_date:
                start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
        except ValueError:
            # Manejar errores de formato de fecha aquí si es necesario
            pass

        
        # Realiza la filtración de acuerdo a las fechas
        if start_date:
            queryset = queryset.filter(registration_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(registration_date__lte=end_date)
        elif start_date and end_date:
            queryset = queryset.filter(registration_date__gte=start_date,date_create__lte=end_date)
        
        # Filtrar por  campos que contengan la palabra clave en su nombre
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(subject__icontains=keyword) | Q(message__icontains=keyword) | Q(attach__icontains=keyword))
        
        if lab:
            queryset = queryset.filter(lab=lab)

        queryset = queryset.order_by('id')
        return queryset
    
# ------------------------------------------- #
# Paginación de solicitudes externas residuos #
class GuardarPerPageViewExternalRequests(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        per_page = kwargs.get('per_page')
        request.session['per_page'] = per_page

        # Redirigir a la página de inventario con los parámetros de filtrado actuales
        filtered_start_date = request.session.get('filtered_start_date')
        filtered_end_date = request.session.get('filtered_end_date')
        filtered_lab = request.session.get('filtered_lab')
        filtered_keyword = request.session.get('filtered_keyword')
        
        url = reverse('residuos:external_requests')
        params = {}
        
        if filtered_start_date:
            params['start_date'] = filtered_start_date
        if filtered_end_date:
            params['end_date'] = filtered_end_date
        if filtered_lab:
            params['lab'] = filtered_lab
        if filtered_keyword:
            params['keyword'] = filtered_keyword
        
        
        if params:
            url += '?' + urlencode(params)

        return redirect(url)

    