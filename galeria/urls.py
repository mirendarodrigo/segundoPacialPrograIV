from django.urls import path
from . import views

urlpatterns = [
    path('', views.galeria_view, name='galeria'),
    path('foto/<int:id>/editar/', views.editar_foto, name='editar_foto'),
    path('foto/<int:id>/borrar/', views.borrar_foto, name='borrar_foto'),
]