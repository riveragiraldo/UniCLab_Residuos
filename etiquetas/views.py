from django.shortcuts import render

from reactivos.views import *
from residuos.views import *
from reactivos.models import *
from residuos.models import *
from .models import *
from .utils import check_group_permission


from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.styles import Border, Side, Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from PIL import Image as PILImage
import openpyxl
from openpyxl import Workbook
import math

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
            numero = request.POST.get('number')
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
            print("Número: ", numero)
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
                numero=int(numero)
                if numero > 56:
                    mensaje= f'Solo es posible generar 56 etiquetas básicas de manera simultanea, revise e intente nuevamente'
                    return JsonResponse({'success': False, 'errors': mensaje})

                mensaje = 'Enlace de etiqueta básica generado correctamente'
                print(mensaje)
                download_url = reverse('etiquetas:download_basic_label')
                # Agregar parámetros a la URL
                download_url = f"{download_url}?substance_name={nombre}&substance_id={id_sustancia}&label_number={numero}"
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
        nombre_sustancia = request.GET.get('substance_name')
        id_sustancia = request.GET.get('substance_id')
        
        numero_etiquetas = int(request.GET.get('label_number'))  # Convertir a entero

        # Verificar si el número de etiquetas es superior a 56
        if numero_etiquetas > 56:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            
            # Mensaje de error
            # Mensaje de error
            error_message = "¡Upps algo ocurrió mal!\nEl número máximo de etiquetas debe ser menor o igual a 56, revisa y genera nuevamente tus etiquetas."

            # Ajustar la celda para el mensaje
            cell = sheet.cell(row=1, column=1)
            cell.value = error_message
            cell.font = Font(name='Arial', size=10, bold=True, color='FF0000')  # Letras llamativas, tamaño más pequeño
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)  # Ajuste de texto y nueva línea
            sheet.merge_cells('A1:E10')  # Unir celdas para el mensaje, aumentando la altura
            sheet.row_dimensions[1].height = 40  # Ajustar la altura de la fila
            sheet.column_dimensions[get_column_letter(1)].width = 50  # Ajustar el ancho de la columna
            
            # Guardar el archivo en la memoria y preparar la respuesta HTTP
            file_name = get_file_name()
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            workbook.save(response)
            return response

        sustancia = get_object_or_404(Sustancias, id=id_sustancia)
        cas = sustancia.cas
        advertencia = sustancia.warning.name
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Definir un relleno con fondo blanco
        white_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

        # Crear un borde de puntos
        thin_border = Side(style='thin')

        # Calcular número de líneas necesarias
        num_lines = math.ceil(numero_etiquetas / 4)
        

        for line in range(num_lines):
            # Calcular el offset de fila para cada línea
            row_offset = line * 9  # 9 filas por etiqueta (8 etiquetas + 1 separación)

            for i in range(4):
                index = line * 4 + i
                if index >= numero_etiquetas:
                    break

                # Calcular el offset de columna para cada etiqueta
                col_offset = i * 7
                
                # Aplicar el fondo blanco a las celdas de la etiqueta actual
                for row in range(1, 9):  # Filas 1 a 8
                    for col in range(1, 7):  # Columnas A a F
                        cell = sheet.cell(row=row + row_offset, column=col + col_offset)
                        cell.fill = white_fill

                # Anchos de columna para cada etiqueta
                sheet.column_dimensions[get_column_letter(1 + col_offset)].width = 1.68  # Ancho = 1
                sheet.column_dimensions[get_column_letter(2 + col_offset)].width = 4.9   # Ancho = 4.27
                sheet.column_dimensions[get_column_letter(3 + col_offset)].width = 3     # Ancho = 2.36 
                sheet.column_dimensions[get_column_letter(4 + col_offset)].width = 2.90  # Ancho 2.27
                sheet.column_dimensions[get_column_letter(5 + col_offset)].width = 5.3   # Ancho 4.64 
                sheet.column_dimensions[get_column_letter(6 + col_offset)].width = 1.68  # Ancho = 1

                # Separador para la siguiente etiqueta a la derecha
                if i < 3:
                    sheet.column_dimensions[get_column_letter(7 + col_offset)].width = 1.55

                # # Ajustar las alturas de las filas
                

                
                
                # Ajustar las alturas de las filas
                sheet.row_dimensions[1 + row_offset].height = 3.8
                sheet.row_dimensions[2 + row_offset].height = 13.5
                sheet.row_dimensions[3 + row_offset].height = 9
                sheet.row_dimensions[4 + row_offset].height = 4.5
                sheet.row_dimensions[5 + row_offset].height = 11.5
                sheet.row_dimensions[6 + row_offset].height = 16
                sheet.row_dimensions[7 + row_offset].height = 29
                sheet.row_dimensions[8 + row_offset].height = 5.3
                # Separador para la siguiente etiqueta abajo
                sheet.row_dimensions[9+ row_offset].height = 8.5

                
                
                
                
                
                # Aplicar bordes manualmente para formar el rectángulo
                # A1: Borde izquierdo y borde arriba
                sheet.cell(row=1 + row_offset, column=1 + col_offset).border = Border(left=thin_border, top=thin_border)

                # A2:A7 Borde izquierdo
                for row in range(2, 8):
                    sheet.cell(row=row + row_offset, column=1 + col_offset).border = Border(left=thin_border)

                # A8 Borde izquierdo y borde abajo
                sheet.cell(row=8 + row_offset, column=1 + col_offset).border = Border(left=thin_border, bottom=thin_border)

                # B1:E1 Borde arriba
                for col in range(2, 6):
                    sheet.cell(row=1 + row_offset, column=col + col_offset).border = Border(top=thin_border)

                # F1: Borde arriba, borde derecho
                sheet.cell(row=1 + row_offset, column=6 + col_offset).border = Border(top=thin_border, right=thin_border)

                # B7:E8 Borde abajo
                for col in range(2, 6):
                    sheet.cell(row=8 + row_offset, column=col + col_offset).border = Border(bottom=thin_border)

                # F8 Borde abajo, borde derecho
                sheet.cell(row=8 + row_offset, column=6 + col_offset).border = Border(bottom=thin_border, right=thin_border)

                # F2:F7 Borde derecho
                for row in range(2, 8):
                    sheet.cell(row=row + row_offset, column=6 + col_offset).border = Border(right=thin_border)

                # Unir celdas B2:E2 y colocar "Nombre de la sustancia"
                sheet.merge_cells(start_row=2 + row_offset, start_column=2 + col_offset, end_row=2 + row_offset, end_column=5 + col_offset)
                merged_cell = sheet.cell(row=2 + row_offset, column=2 + col_offset)
                merged_cell.value = nombre_sustancia.upper()  # Normalizar a mayúscula
                merged_cell.alignment = Alignment(horizontal='center', vertical='center', shrink_to_fit=True)  # Formato "Reducir hasta ajustar"
                merged_cell.font = Font(name='Ancizar Sans', size=10)  # Fuente y tamaño

                # Unir celdas B3:C3 y colocar "CAS"
                sheet.merge_cells(start_row=3 + row_offset, start_column=2 + col_offset, end_row=3 + row_offset, end_column=3 + col_offset)
                merged_cell = sheet.cell(row=3 + row_offset, column=2 + col_offset)
                merged_cell.value = 'CAS'
                merged_cell.alignment = Alignment(horizontal='center', vertical='center', shrink_to_fit=True)  # Formato "Reducir hasta ajustar"
                merged_cell.font = Font(name='Ancizar Sans', size=8)  # Fuente y tamaño

                # Unir celdas D3:E3 y colocar CAS de la sustancia
                sheet.merge_cells(start_row=3 + row_offset, start_column=4 + col_offset, end_row=3 + row_offset, end_column=5 + col_offset)
                merged_cell = sheet.cell(row=3 + row_offset, column=4 + col_offset)
                merged_cell.value = cas.upper()  # Normalizar a mayúscula
                merged_cell.alignment = Alignment(horizontal='center', vertical='center', shrink_to_fit=True)  # Formato "Reducir hasta ajustar"
                merged_cell.font = Font(name='Ancizar Sans', size=8)  # Fuente y tamaño

                # Unir celdas B4:B7, girar 90° a la izquierda y colocar palabra de advertencia en mayúscula y negrita
                sheet.merge_cells(start_row=4 + row_offset, start_column=2 + col_offset, end_row=7 + row_offset, end_column=2 + col_offset)
                merged_cell = sheet.cell(row=4 + row_offset, column=2 + col_offset)
                merged_cell.value = advertencia.upper()  # Normalizar a mayúscula
                merged_cell.alignment = Alignment(horizontal='center', vertical='center', shrink_to_fit=True, text_rotation=90)  # Girar texto 90°
                merged_cell.font = Font(name='Ancizar Sans', size=9, bold=True)  # Fuente, tamaño y negrita

                # C5: Agregar el pictograma1 si existe
                if sustancia and sustancia.pictogram_clp1:
                    fila_picto=4+row_offset
                    pictogram_path = sustancia.pictogram_clp1.pictogram.path
                    img = openpyxl.drawing.image.Image(pictogram_path)
                    img.height = 40  # Ajuste Altura
                    img.width = 40   # Ajuste Ancho
                    img.anchor = f'{get_column_letter(3 + col_offset)}{fila_picto}'
                    sheet.add_image(img)
                
                # C7: Agregar el pictograma2 si existe
                if sustancia and sustancia.pictogram_clp2:
                    fila_picto=7+row_offset
                    pictogram_path = sustancia.pictogram_clp2.pictogram.path
                    img = openpyxl.drawing.image.Image(pictogram_path)
                    img.height = 40  # Ajuste Altura
                    img.width = 40   # Ajuste Ancho
                    img.anchor = f'{get_column_letter(3 + col_offset)}{fila_picto}'
                    sheet.add_image(img)

                # D6: Agregar el pictograma3 si existe
                if sustancia and sustancia.pictogram_clp3:
                    fila_picto=6+row_offset
                    pictogram_path = sustancia.pictogram_clp3.pictogram.path
                    img = openpyxl.drawing.image.Image(pictogram_path)
                    img.height = 40  # Ajuste Altura
                    img.width = 40   # Ajuste Ancho
                    img.anchor = f'{get_column_letter(4 + col_offset)}{fila_picto}'
                    sheet.add_image(img)

                # E4: Agregar el pictograma4 si existe
                if sustancia and sustancia.pictogram_clp4:
                    fila_picto=4+row_offset
                    pictogram_path = sustancia.pictogram_clp4.pictogram.path
                    img = openpyxl.drawing.image.Image(pictogram_path)
                    img.height = 40  # Ajuste Altura
                    img.width = 40   # Ajuste Ancho
                    img.anchor = f'{get_column_letter(5 + col_offset)}{fila_picto}'
                    sheet.add_image(img)

                # E7: Agregar el pictograma5 si existe
                if sustancia and sustancia.pictogram_clp5:
                    fila_picto=7+row_offset
                    pictogram_path = sustancia.pictogram_clp5.pictogram.path
                    img = openpyxl.drawing.image.Image(pictogram_path)
                    img.height = 40  # Ajuste Altura
                    img.width = 40   # Ajuste Ancho
                    img.anchor = f'{get_column_letter(5 + col_offset)}{fila_picto}'
                    sheet.add_image(img)
        
        # Guardar el archivo en la memoria y preparar la respuesta HTTP
        file_name = get_file_name()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        workbook.save(response)
        return response





