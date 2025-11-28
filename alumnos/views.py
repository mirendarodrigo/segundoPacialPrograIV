import io
import threading # <--- IMPORTANTE
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Alumno
from .forms import AlumnoForm

# ReportLab
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# --- FUNCIÓN AUXILIAR PARA ENVIAR PDF EN SEGUNDO PLANO ---
def enviar_pdf_async(asunto, cuerpo, origen, destino, nombre_archivo, contenido_pdf):
    try:
        email = EmailMessage(
            asunto,
            cuerpo,
            origen,
            destino,
        )
        # Adjuntamos el PDF (nombre, bytes, tipo mime)
        email.attach(nombre_archivo, contenido_pdf, 'application/pdf')
        email.send(fail_silently=True)
        print(f">>> PDF de {nombre_archivo} enviado con éxito en segundo plano.")
    except Exception as e:
        print(f">>> Error enviando PDF: {e}")

# ===========================================================
# VISTAS
# ===========================================================

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

    # 1. Generar PDF en Memoria (Esto es rápido, lo hacemos aquí)
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
    
    # Obtenemos los bytes del PDF
    pdf_content = buffer.getvalue()
    buffer.close()

    # 2. Enviar por correo usando THREADING (Segundo Plano)
    # Definimos el destino: el usuario logueado o el propio alumno (según prefieras)
    email_destino = [request.user.email] 
    
    task = threading.Thread(
        target=enviar_pdf_async,
        args=(
            f'Reporte PDF de {alumno.nombre}',            # Asunto
            'Adjunto encontrarás la ficha del alumno.',   # Cuerpo
            settings.EMAIL_HOST_USER,                     # Origen
            email_destino,                                # Destino
            f'alumno_{alumno.id}.pdf',                    # Nombre Archivo
            pdf_content                                   # Contenido (Bytes)
        )
    )
    task.start() # ¡Dispara y olvida!

    # 3. Redirigir inmediatamente (Usuario feliz)
    return redirect('listar_alumnos')