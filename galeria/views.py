from django.shortcuts import render, redirect , get_object_or_404
from .models import Foto
from .forms import FotoForm

def galeria_view(request):
    if request.method == 'POST':
        # IMPORTANTE: request.FILES es necesario para recibir archivos
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = FotoForm()

    fotos = Foto.objects.all()
    return render(request, 'galeria/index.html', {'form': form, 'fotos': fotos})

# EDITAR FOTO
def editar_foto(request, id):
    foto = get_object_or_404(Foto, id=id)
    
    if request.method == 'POST':
        # Pasamos instance=foto para editar, y request.FILES por si cambia la imagen
        form = FotoForm(request.POST, request.FILES, instance=foto)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = FotoForm(instance=foto)
    
    return render(request, 'galeria/editar.html', {'form': form, 'foto': foto})

# BORRAR FOTO
def borrar_foto(request, id):
    foto = get_object_or_404(Foto, id=id)
    if request.method == 'POST':
        foto.delete() 
        # Nota: Por defecto Django borra el registro de la DB, 
        # pero a veces el archivo queda en disco. Para un parcial está bien así.
        return redirect('galeria')
    
    return render(request, 'galeria/borrar.html', {'foto': foto})