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
    
# ---------------------------------------------------------- #
# Paginación de listado de clasifición de residuos
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


# ---------------------------------------------------------- #
# Autocompletado de clasificaciones

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
            return f'clasificacion_residuos_decreto_1076_2015_{now.strftime("%d%m%Y%H%M%S")}.xlsx'
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
                
                # Registrar evento
                tipo_evento = 'CREAR REGISTRO DE RESIDUOS'
                usuario_evento = request.user
                crear_evento(tipo_evento, usuario_evento)
                
                mensaje = 'Registro de residuo creado correctamente.'
                return JsonResponse({'success': True, 'message': mensaje})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print(e)
            mensaje = f'Error: {e}'
            return HttpResponseBadRequest(f'Error interno del servidor: {mensaje}')