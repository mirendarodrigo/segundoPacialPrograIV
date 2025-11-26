import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def buscar_view(request):
    data = None
    error = None
    mensaje = None

    # ---------------------------------------------------------
    # LÓGICA DE ENVÍO DE CORREO (POST)
    # ---------------------------------------------------------
    if request.method == 'POST':
        titulo = request.POST.get('titulo_hidden')
        descripcion = request.POST.get('desc_hidden')
        
        # Si el usuario está logueado usa su email, si no, uno por defecto o el del admin
        email_destino = request.user.email if request.user.is_authenticated else settings.EMAIL_HOST_USER

        try:
            send_mail(
                f'Resultado Scraping: {titulo}',
                f'Aquí tienes el resumen encontrado:\n\n{descripcion}',
                settings.EMAIL_HOST_USER,
                [email_destino],
                fail_silently=False,
            )
            mensaje = "¡El resultado ha sido enviado a tu correo!"
        except Exception as e:
            error = f"Error al enviar el correo: {str(e)}"

    # ---------------------------------------------------------
    # LÓGICA DE SCRAPING (GET)
    # ---------------------------------------------------------
    query = request.GET.get('q')

    if query:
        url = "https://es.wikipedia.org/w/index.php"
        params = {'search': query}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                titulo_tag = soup.find('h1', {'id': 'firstHeading'})
                titulo = titulo_tag.text if titulo_tag else "Sin título"

                if "Resultados de la búsqueda" in titulo:
                    error = "La búsqueda fue ambigua. Intenta ser más específico."
                else:
                    imagen_url = None
                    tabla_info = soup.find('table', {'class': 'infobox'})
                    if tabla_info:
                        img_tag = tabla_info.find('img')
                        if img_tag:
                            imagen_url = "https:" + img_tag['src']

                    descripcion = "No se encontró descripción."
                    parrafos = soup.find_all('p')
                    for p in parrafos:
                        if p.text and len(p.text) > 60:
                            descripcion = p.text
                            break

                    data = {
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'imagen': imagen_url,
                        'url_origen': response.url
                    }
            else:
                error = "No se pudo acceder a Wikipedia."

        except Exception as e:
            error = "Ocurrió un error inesperado de conexión."

    return render(request, 'scraper/buscar.html', {'data': data, 'error': error, 'mensaje': mensaje})