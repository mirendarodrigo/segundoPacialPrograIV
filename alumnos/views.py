import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Alumno
from .forms import AlumnoForm 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

@login_required
def listar_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/lista.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/form.html', {'form': form})

@login_required
def enviar_pdf_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)

    # 1. Generar PDF en Memoria (Buffer)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Ficha de Alumno: {alumno.nombre}", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Legajo: {alumno.legajo}", styles['Normal']))
    elements.append(Paragraph(f"Carrera: {alumno.carrera}", styles['Normal']))
    elements.append(Paragraph(f"Email: {alumno.email}", styles['Normal']))

    doc.build(elements)
    
    # 2. Obtener el valor binario del PDF
    pdf_content = buffer.getvalue()
    buffer.close()

    # 3. Armar el correo con adjunto
    email = EmailMessage(
        f'Reporte PDF de {alumno.nombre}', # Asunto
        'Adjunto encontrarás la ficha del alumno solicitado.', # Cuerpo
        settings.EMAIL_HOST_USER, # Desde
        [request.user.email], # Hacia (se lo mandamos al usuario logueado)
    )
    
    # Adjuntamos: nombre_archivo, contenido, tipo mime
    email.attach(f'alumno_{alumno.id}.pdf', pdf_content, 'application/pdf')
    email.send()

    return redirect('listar_alumnos')