from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_tareas, name='listar_tareas'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('<int:id>/editar/', views.editar_tarea, name='editar_tarea'),
    path('<int:id>/borrar/', views.borrar_tarea, name='borrar_tarea'),
]