import os
from modules.db import BaseDatos

def cargar_corpus_inicial():
    db = BaseDatos()
    corpus_dir = "data/corpus/"
    
    if not os.path.exists(corpus_dir):
        print("❌ No se encontró la carpeta de corpus.")
        return

    archivos = [f for f in os.listdir(corpus_dir) if f.endswith('.txt')]
    print(f"--- Cargando {len(archivos)} documentos a la base de datos ---")

    for nombre_archivo in archivos:
        ruta = os.path.join(corpus_dir, nombre_archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            # Asumimos que la primera línea es la FUENTE del scraper
            fuente = lineas[0].replace("FUENTE: ", "").strip() if lineas else "Desconocida"
            contenido = "".join(lineas[1:]).strip()
            
            db.insertar_documento(nombre_archivo, contenido, fuente)
            print(f"✅ Cargado: {nombre_archivo}")

    print("\n--- ¡Base de datos inicializada con éxito! ---")
    db.cerrar()

if __name__ == "__main__":
    cargar_corpus_inicial()