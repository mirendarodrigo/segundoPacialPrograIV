from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea
from .forms import TareaForm

# 1. LISTAR (Read)
def listar_tareas(request):
    tareas = Tarea.objects.all().order_by('-fecha_creacion')
    return render(request, 'tareas/listar.html', {'tareas': tareas})

# 2. CREAR (Create)
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/form.html', {'form': form, 'titulo': 'Nueva Tarea'})

# 3. EDITAR (Update)
def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id) # Busca o da error 404
    if request.method == 'POST':
        # Pasamos 'instance=tarea' para que edite esa y no cree una nueva
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('listar_tareas')
    else:
        form = TareaForm(instance=tarea) # Pre-llenamos el form
    return render(request, 'tareas/form.html', {'form': form, 'titulo': 'Editar Tarea'})

# 4. BORRAR (Delete)
def borrar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('listar_tareas')
    return render(request, 'tareas/borrar.html', {'tarea': tarea})