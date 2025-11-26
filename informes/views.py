import io
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Reporte

# IMPORTACIONES PARA EL PDF (Platypus)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# 1. Vista para listar (Esta es la que te faltaba si borraste todo)
def listar_reportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'informes/lista.html', {'reportes': reportes})

# 2. Vista que GENERA el PDF (Versión corregida con párrafos automáticos)
def generar_pdf(request, id):
    # a) Buscar el reporte
    reporte = get_object_or_404(Reporte, id=id)

    # b) Crear el Buffer
    buffer = io.BytesIO()

    # c) Configurar el Documento (Platypus)
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # d) Crear la lista de elementos
    elements = []
    styles = getSampleStyleSheet()

    # --- AGREGANDO CONTENIDO ---

    # Título
    elements.append(Paragraph(f"Reporte: {reporte.nombre}", styles['Title']))
    elements.append(Spacer(1, 12)) 

    # Fecha
    elements.append(Paragraph(f"Fecha de emisión: {reporte.fecha}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Contenido (Manejo de saltos de línea y párrafos largos)
    parrafos = reporte.contenido.split('\n')
    
    for texto in parrafos:
        if texto.strip(): # Solo si hay texto
            elements.append(Paragraph(texto, styles['Normal']))
            elements.append(Spacer(1, 12)) 

    # e) Construir
    doc.build(elements)

    # f) Retornar
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'reporte_{id}.pdf')