from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_reportes, name='listar_reportes'),
    path('pdf/<int:id>/', views.generar_pdf, name='generar_pdf'),
]