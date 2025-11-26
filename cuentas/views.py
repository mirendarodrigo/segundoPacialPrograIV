import threading # <--- 1. IMPORTANTE: Necesario para el segundo plano
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm

# --- FUNCIÓN AUXILIAR PARA ENVIAR MAIL EN SEGUNDO PLANO ---
def enviar_mail_async(asunto, mensaje, origen, destino):
    """
    Esta función se ejecutará en un hilo paralelo.
    Si falla, no rompe la página web.
    """
    try:
        send_mail(asunto, mensaje, origen, destino, fail_silently=True)
        print(">>> Mail enviado en segundo plano con éxito.")
    except Exception as e:
        print(f">>> Error enviando mail: {e}")

# ===========================================================
# VISTAS
# ===========================================================

# 1. REGISTRO (CON THREADING)
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # --- LÓGICA DE HILOS (Anti-Timeout) ---
            asunto = '¡Bienvenido al Parcial!'
            mensaje = f'Hola {user.username}, gracias por registrarte en nuestra plataforma.'
            email_destino = [user.email]
            
            # Creamos el hilo
            task = threading.Thread(
                target=enviar_mail_async,
                args=(asunto, mensaje, settings.EMAIL_HOST_USER, email_destino)
            )
            # Iniciamos el hilo (La web sigue cargando sin esperar a Gmail)
            task.start()
            # --------------------------------------

            return redirect('login') 
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

# 2. LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') # O a 'panel'
    else:
        form = AuthenticationForm()
    return render(request, 'cuentas/login.html', {'form': form})

# 3. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')

# 4. PANEL
@login_required
def panel_view(request):
    return render(request, 'cuentas/panel.html')