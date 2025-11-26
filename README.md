# 🚀 Segundo Parcial - Programación IV (Django)

Este proyecto es una aplicación web full-stack desarrollada con **Django**, diseñada para gestionar alumnos, generar reportes PDF y realizar scraping de datos educativos, con integración de notificaciones por correo electrónico.

🔗 **Link al Deploy (Render):** https://segundopacialprograiv.onrender.com/

---

## 📋 Características Principales

### 1. 🔐 Autenticación y Usuarios
- Sistema de **Login, Registro y Logout** nativo de Django.
- Envío automático de **email de bienvenida** al registrarse.
- Control de acceso: Las funcionalidades principales requieren estar logueado.

### 2. 🎓 Gestión de Alumnos (Dashboard)
- **CRUD Completo:** Alta, baja y modificación de alumnos (Nombre, Legajo, Carrera).
- **Generación de PDF:** Creación dinámica de fichas de alumnos usando `ReportLab`.
- **Envío por Correo:** Botón para enviar la ficha PDF adjunta directamente al email del usuario.

### 3. 🔍 Scraper Educativo (Wikipedia)
- Buscador integrado que consulta la API/Web de **Wikipedia** en tiempo real.
- Visualización de título, imagen y resumen del artículo.
- Funcionalidad para **enviar el resultado de la investigación** por correo electrónico.

### 4. ☁️ Despliegue (Producción)
- Configurado para **Render**.
- Base de datos **PostgreSQL** en producción (SQLite en local).
- Archivos estáticos servidos con **WhiteNoise**.
- Variables de entorno seguras.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3, Django 5.
- **Frontend:** HTML5, Bootstrap 5.
- **Base de Datos:** SQLite (Dev) / PostgreSQL (Prod).
- **Librerías Clave:**
    - `reportlab`: Generación de PDFs.
    - `beautifulsoup4` & `requests`: Web Scraping.
    - `django-environ`: Manejo de variables de entorno.
    - `gunicorn` & `whitenoise`: Servidor de producción.

---

## ⚙️ Instalación y Ejecución Local

Sigue estos pasos para correr el proyecto en tu máquina:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/mirendarodrigo/segundoPacialPrograIV
   cd segundoParcial

Crear y activar entorno virtual:


  ```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
Instalar dependencias:
```
  ```bashh

pip install -r requirements.txt
```
Configurar Variables de Entorno (.env): Crea un archivo .env en la raíz y configura tus credenciales:

  ```bash

DEBUG=True
SECRET_KEY=clave-secreta-local
EMAIL_USER=tu_gmail@gmail.com
EMAIL_PASS=tu_contraseña_de_aplicacion
ADMIN_PASSWORD=admin1234
```
Migrar base de datos:

  ```bash

python manage.py migrate
Crear Superusuario (Script automático):
```
  ```bash

python crear_admin.py
```
# O manualmente: python manage.py createsuperuser
Ejecutar servidor:

  ```bash

python manage.py runserver
```
📂 Estructura del Proyecto
El proyecto está modularizado en las siguientes aplicaciones:

segundoParcial/: Configuración principal (Settings, URLs).

cuentas/: Manejo de usuarios (Auth).

alumnos/: Lógica de estudiantes y generación de PDFs.

scraper/: Lógica de conexión con Wikipedia.

templates/: Plantillas HTML globales.

👤 Autor
Mirenda Rodrigo Programación IV - CUDI Fecha: 26 Noviembre 2025
