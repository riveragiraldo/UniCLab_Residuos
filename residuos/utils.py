import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings


# Utilidad que realiza la conversión a PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Utilidad que realiza la conversión a PDF y lo guarda en el sistema de archivos
def render_to_pdf_file(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        # Define the path and filename for the PDF
        pdf_filename = f'solicitud_{context_dict["solicitud"].pk}.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

        # Write the PDF to a file
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(result.getvalue())

        return pdf_filename
    return None