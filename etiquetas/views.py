from django.shortcuts import render

from reactivos.views import *
from residuos.views import *
from reactivos.models import *
from residuos.models import *
from .models import *
from .utils import check_group_permission


# -------------------------------------------- #
# Vista para la descarga del formato en blanco #
class DownloadFormatLabelView(LoginRequiredMixin, View):
    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def get(self, request, *args, **kwargs):
        try:
            configuracion_sistema = ConfiguracionSistema.objects.first()

            if configuracion_sistema and configuracion_sistema.formato_libre:
                formato = configuracion_sistema.formato_libre
                filename = formato.name.split('/')[-1]

                # Crear una respuesta de archivo directamente con FileResponse
                response = FileResponse(formato.open(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

                # Registro de mensaje (opcional)
                mensaje = f'Se ha descargado el archivo {filename}'
                print(mensaje)

                return response
            else:
                return HttpResponse("El formato no está disponible en este momento.", status=404)
        except Exception as e:
            return HttpResponse(f"Error al descargar el formato: {str(e)}", status=500)


# ----------------------------------------------------------------- #
# Vista para la generación de las etiquetas de susrtancias químicas #

class GenerateLabel(LoginRequiredMixin, View):
    template_name = 'Etiquetas/generar_etiquetas.html'
    
    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def get(self, request, *args, **kwargs):
        context = {
            'labs': Laboratorios.objects.all(),
        }
        return render(request, self.template_name, context)

    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def post(self, request, *args, **kwargs):
        
        try:
            # Obtener los valores de los campos del formulario
            nombre = request.POST.get('reagent')
            cas = request.POST.get('cas')
            id_sustancia = request.POST.get('id_reagent')
            etiqueta = request.POST.get('label_type')
            laboratorio = request.POST.get('lab')
            id_hermes = request.POST.get('ID_Hermes')
            telefono_emergencia = request.POST.get('emergency_number')
            # Verificar estado del checkbox
            formato_libre = request.POST.get('empty_template')
            formato_libre_estado = True if formato_libre == 'on' else False
            # Imprimir los valores en la terminal
            print("Nombre:", nombre)
            print("CAS:", cas)
            print("ID Sustancia:", id_sustancia)
            print("Etiqueta:", etiqueta)
            print("Laboratorio:", laboratorio)
            print("ID Hermes:", id_hermes)
            print("Teléfono Emergencia:", telefono_emergencia)
            print("Formato Libre:", formato_libre_estado)
            # try:
            # Si formato_libre_estado es True, descargar el formato libre
            if formato_libre_estado:
                mensaje='Generando'

                print(mensaje)
                # return redirect('etiquetas:download_format')
                return JsonResponse({'success': True, 'message': mensaje})

            # Verificar campos necesarios
            if not nombre or not id_sustancia or not etiqueta:
                mensaje = 'Error: Los campos Nombre, ID Sustancia y Etiqueta son obligatorios.'
                print(mensaje)
                return JsonResponse({'success': False, 'errors': mensaje})

            # Verificación adicional para el número de teléfono
            if telefono_emergencia and not re.match(r'^(60\d{8}|3\d{9})$', telefono_emergencia):
                mensaje = 'Error: Ingrese un número telefónico válido para Colombia (60xxxxxxxx o 3xxxxxxxxx).'
                print(mensaje)
                return JsonResponse({'success': False, 'message': mensaje})

            # Funcionalidad basada en la etiqueta seleccionada
            if etiqueta == '1':
                mensaje = 'Funcionalidad de etiqueta básica'
                print(mensaje)
                download_url = reverse('etiquetas:download_basic_label')
                # Agregar parámetros a la URL
                download_url = f"{download_url}?lab={laboratorio}&substance_name={nombre}&substance_id={id_sustancia}&hermes_id={id_hermes}&e_number={telefono_emergencia}"
                print(download_url)
                messages.success(self.request, f'{download_url}')
                return JsonResponse({'success': True, 'message': mensaje})



            elif etiqueta == '2':
                mensaje = 'Funcionalidad de etiqueta mediana'
                print(mensaje)
                return JsonResponse({'success': True, 'message': mensaje})
            elif etiqueta == '3':
                mensaje = 'Funcionalidad de etiqueta pequeña'
                print(mensaje)
                return JsonResponse({'success': True, 'message': mensaje})
            elif etiqueta == '4':
                mensaje = 'Funcionalidad de etiqueta grande'
                print(mensaje)
                return JsonResponse({'success': True, 'message': mensaje})

            # Si no se cumple ninguno de los casos de etiqueta
            mensaje = 'Error: Tipo de etiqueta no válido.'
            print(mensaje)
            return JsonResponse({'success': False, 'message': mensaje})
        
        except Exception as e:
            # Manejo de cualquier excepción no prevista
            mensaje = f'Error: Ocurrió un problema inesperado. Detalles: {str(e)}'
            print(mensaje)
            return JsonResponse({'success': False, 'message': mensaje})

                
                
           
            
           
    
# ------------------------------------ #
# Autocompletado de sustancias químicas #

class autocompleteChemicalSubstances(LoginRequiredMixin,View):
    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def get(self, request):
        term = request.GET.get('term', '')
        
        substances = Sustancias.objects.filter(
                Q(name__icontains=term) | Q(cas__icontains=term)).order_by('name')[:20]
        

        results = []
        for substance in substances:
            result = {
                'name': substance.name,
                'cas': substance.cas,
                'id_substance':substance.id,
            }
            results.append(result)
        return JsonResponse(results, safe=False)
    

# ----------------------- #
# Generar Etiqueta Básica #
class GenerateBasicLabel(LoginRequiredMixin, View):
    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
       
    @check_group_permission(groups_required=['ADMINISTRADOR'])
    def get(self, request, *args, **kwargs):
        def get_file_name():
            now = datetime.now()
            return f'Etiqueta_básica_{now.strftime("%d%m%Y%H%M%S")}.xlsx'
        
        # Extraer parámetros de la URL
        laboratorio = request.GET.get('lab')
        nombre_sustancia = request.GET.get('substance_name')
        id_sustancia = request.GET.get('substance_id')
        id_hermes = request.GET.get('hermes_id')
        telefono_emergencia = request.GET.get('e_number')
        
        print('Hola Mundo')
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        logo_path = finders.find('inventarioreac/Images/escudoUnal_black.png')
        pil_image = PILImage.open(logo_path)
        image = ExcelImage(pil_image)
        sheet.add_image(image, 'A1')

        fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        sheet['C1'] = 'Listado de registro de residuos'
        sheet['C2'] = 'Fecha de Creación: '+fecha_creacion
        sheet['A4'] = 'ID Solicitud'
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
        
        # Agregar datos de la etiqueta
        sheet['A5'] = id_sustancia
        sheet['B5'] = laboratorio
        sheet['C5'] = nombre_sustancia
        sheet['D5'] = 'N/A'
        sheet['E5'] = 'N/A'
        sheet['F5'] = 'N/A'
        sheet['G5'] = 'N/A'
        sheet['H5'] = 'N/A'
        sheet['I5'] = 'N/A'
        sheet['J5'] = 'N/A'
        sheet['K5'] = request.user.username

        # Si hay datos adicionales, agregarlos también
        if id_hermes:
            sheet['A6'] = 'ID Hermes'
            sheet['B6'] = id_hermes

        if telefono_emergencia:
            sheet['A7'] = 'Teléfono de Emergencia'
            sheet['B7'] = telefono_emergencia

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

