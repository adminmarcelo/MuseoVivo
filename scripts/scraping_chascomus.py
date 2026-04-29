import requests
from bs4 import BeautifulSoup
import os
import time
import random
from urllib.parse import urlparse

# Configuración de ruta según la estructura del proyecto [cite: 83]
CORPUS_PATH = "data/corpus/"

# Lista completa de URLs para MuseoVivo
urls_proyecto = [
    "https://guiachascomus.com.ar/alojamientos-chascomus/",
    "https://guiachascomus.com.ar/guia-de-comercios-y-servicios/gastronomia/",
    "https://guiachascomus.com.ar/guia-de-comercios-y-servicios/regionales/",
    "https://guiachascomus.com.ar/guia-de-comercios-y-servicios/tiendas-comercios/",
    "https://guiachascomus.com.ar/guia-de-comercios-y-servicios/aire-libre-diversion/",
    "https://guiachascomus.com.ar/castillo-amistad-chascomus/",
    "https://guiachascomus.com.ar/arquitectura-chascomus/",
    "https://guiachascomus.com.ar/chascomus-capital-del-pejerrey/",
    "https://guiachascomus.com.ar/alfonsin-chascomus/",
    "https://guiachascomus.com.ar/capilla-negros-chascomus/",
    "https://guiachascomus.com.ar/que-hacer-chascomus-con-chicos/",
    "https://guiachascomus.com.ar/semana-santa-chascomus/",
    "https://guiachascomus.com.ar/casa-casco-chascomus/",
    "https://guiachascomus.com.ar/estacion-hidrobiologica-chascomus/",
    "https://guiachascomus.com.ar/historia-chascomus/",
    "https://guiachascomus.com.ar/torii-chascomus/",
    "https://guiachascomus.com.ar/club-pelota-chascomus/",
    "https://guiachascomus.com.ar/catedral-chascomus/",
    "https://guiachascomus.com.ar/cabanas-chascomus/",
    "https://guiachascomus.com.ar/reloj-italianos-chascomus/",
    "https://guiachascomus.com.ar/conecta-naturaleza-chascomus/",
    "https://guiachascomus.com.ar/actividades-en-pareja-chascomus/",
    "https://guiachascomus.com.ar/10-razones-escapada-chascomus/",
    "https://guiachascomus.com.ar/fiestas-tradicionales-chascomus/",
    "https://guiachascomus.com.ar/bigua-ave-emblema-chascomus/",
    "https://guiachascomus.com.ar/cementerio-protestante-chascomus/",
    "https://guiachascomus.com.ar/laguna-chascomus/",
    "https://guiachascomus.com.ar/vieja-estacion-chascomus/",
    "https://guiachascomus.com.ar/espigon-chascomus-pesca-atardeceres/",
    "https://guiachascomus.com.ar/chascomus-laguna-windsurf/",
    "https://destinochascomus.com/atractivos/"
]

# User-Agents para evitar que el servidor nos bloquee rápido
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/123.0.0.0"
]

def limpiar_texto(soup):
    """Limpia el HTML para dejar solo el contenido útil para PLN."""
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'iframe']):
        element.decompose()
    main_content = soup.find('article') or soup.find('main') or soup.find('body')
    return ' '.join(main_content.get_text(separator=' ').split())

def ejecutar_scraping_manual():
    if not os.path.exists(CORPUS_PATH):
        os.makedirs(CORPUS_PATH)

    print(f"--- Iniciando construcción de corpus para MuseoVivo ---")
    
    for i, url in enumerate(urls_proyecto):
        print(f"\n--- URL ({i+1}/{len(urls_proyecto)}): {url} ---")
        input("Presioná Enter para descargar...")
        
        try:
            # Seleccionamos un navegador al azar para cada petición
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            
            # Agregamos una pausa aleatoria antes de la petición
            time.sleep(random.uniform(2, 4))
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 429:
                print("❌ ERROR 429: El servidor bloqueó la petición por exceso de velocidad.")
                print("Sugerencia: Esperá 2 minutos o usá los datos del celular (IP distinta).")
                continue

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            texto = limpiar_texto(soup)
            path_parts = urlparse(url).path.strip('/').split('/')
            nombre_archivo = f"doc_{i+1}_{path_parts[-1].replace('-', '_') if path_parts[-1] else 'index'}.txt"
            
            ruta_final = os.path.join(CORPUS_PATH, nombre_archivo)
            with open(ruta_final, "w", encoding="utf-8") as f:
                f.write(f"FUENTE: {url}\n\n{texto}")
            
            print(f"✅ Guardado: {nombre_archivo}")
            
        except Exception as e:
            print(f"❌ Error procesando esta URL: {e}")

if __name__ == "__main__":
    ejecutar_scraping_manual()