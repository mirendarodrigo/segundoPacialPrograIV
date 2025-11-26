from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm
from django.core.mail import send_mail
from django.conf import settings


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                send_mail(
                    '¡Bienvenido al Parcial!',
                    f'Hola {user.username}, gracias por registrarte en nuestra plataforma.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
            except:
                pass 
            
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')          
            user = authenticate(username=username, password=password)
            if user is not None:    
                login(request, user)
                return redirect('panel')
    else:
        form = AuthenticationForm()
    return render(request, 'cuentas/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def panel_view(request):
    return render(request, 'cuentas/panel.html')