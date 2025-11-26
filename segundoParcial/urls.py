from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings               
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('cuentas/', include('cuentas.urls')),
    path('tareas/', include('tareas.urls')),
    path('galeria/', include('galeria.urls')),
    path('informes/', include('informes.urls')),
    path('scraper/', include('scraper.urls')),
    path('alumnos/', include('alumnos.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)