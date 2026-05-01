import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.db import BaseDatos  # Importamos para el auto-entrenamiento

class MotorBusqueda:
    def __init__(self):
        # Usamos TF-IDF para pesar los términos
        self.vectorizador = TfidfVectorizer()
        self.metadata = [] 
        self.tfidf_matrix = None
        
        # Auto-entrenamiento al inicializar
        self.entrenar_con_db(BaseDatos())

    def entrenar_con_db(self, db_instancia):
        """Carga el conocimiento desde SQLite y construye el índice."""
        try:
            db_instancia.cursor.execute("SELECT titulo, contenido, fuente FROM conocimiento")
            filas = db_instancia.cursor.fetchall()
            
            if not filas:
                print("⚠️ No hay documentos en la base de datos para entrenar.")
                return

            textos = [f"{f[0]} {f[1]}" for f in filas]
            self.metadata = [{"titulo": f[0], "fuente": f[2], "contenido": f[1]} for f in filas]
            
            self.tfidf_matrix = self.vectorizador.fit_transform(textos)
            print(f"✅ Motor de búsqueda entrenado con {len(textos)} documentos.")
        except Exception as e:
            print(f"❌ Error al entrenar el motor: {e}")

    def buscar_mas_relevante(self, consulta_texto):
        """
        MÉTODO PUENTE PARA app.py: 
        Implementa búsqueda por similitud del coseno y devuelve el mejor resultado.
        """
        if self.tfidf_matrix is None:
            return {"contenido": "Error: Motor no entrenado"}, 0.0

        # Transformamos la consulta (el texto directo que viene de app.py)
        query_vector = self.vectorizador.transform([consulta_texto])
        
        # Calculamos similitudes
        similitudes = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Obtenemos el índice del mejor resultado
        idx_mejor = similitudes.argmax()
        score = round(float(similitudes[idx_mejor]), 4)
        
        if score > 0.1: # Umbral mínimo de relevancia
            return self.metadata[idx_mejor], score
        
        return {"contenido": "No se encontró información relevante."}, 0.0 