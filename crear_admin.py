import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "segundoParcial.settings")
django.setup()

from django.contrib.auth.models import User
from django.conf import settings

def crear_usuario():
    # Datos del superusuario (Cámbialos si quieres)
    USERNAME = 'admin'
    EMAIL = 'admin@parcial.com'
    PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin1234') # Lee de variable de entorno o usa default

    if not User.objects.filter(username=USERNAME).exists():
        print(f"Creando superusuario {USERNAME}...")
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print("¡Superusuario creado con éxito!")
    else:
        print(f"El usuario {USERNAME} ya existe. Omitiendo creación.")

if __name__ == "__main__":
    crear_usuario()