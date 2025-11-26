from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_alumnos, name='listar_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('enviar-pdf/<int:id>/', views.enviar_pdf_alumno, name='enviar_pdf'),
]