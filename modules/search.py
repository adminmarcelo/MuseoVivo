import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MotorBusqueda:
    def __init__(self):
        # Usamos TF-IDF para pesar los términos [cite: 48]
        self.vectorizador = TfidfVectorizer()
        self.corpus_procesado = []
        self.metadata = [] # Para guardar títulos y fuentes
        self.tfidf_matrix = None

    def entrenar_con_db(self, db_instancia):
        """Carga el conocimiento desde SQLite y construye el índice invertido[cite: 47, 56]."""
        db_instancia.cursor.execute("SELECT titulo, contenido, fuente FROM conocimiento")
        filas = db_instancia.cursor.fetchall()
        
        textos = [f"{f[0]} {f[1]}" for f in filas] # Combinamos título y contenido
        self.metadata = [{"titulo": f[0], "fuente": f[2], "contenido": f[1]} for f in filas]
        
        if textos:
            self.tfidf_matrix = self.vectorizador.fit_transform(textos)
            print(f"✅ Motor de búsqueda entrenado con {len(textos)} documentos.")

    def buscar(self, consulta_tokens, top_n=3):
        """Implementa búsqueda por similitud del coseno[cite: 49]."""
        if self.tfidf_matrix is None:
            return []

        # Convertimos la consulta del usuario a vector TF-IDF
        query_str = " ".join(consulta_tokens)
        query_vector = self.vectorizador.transform([query_str])
        
        # Calculamos similitudes
        similitudes = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Obtenemos los índices de los mejores resultados
        indices_top = similitudes.argsort()[-top_n:][::-1]
        
        resultados = []
        for idx in indices_top:
            if similitudes[idx] > 0.1: # Umbral mínimo de relevancia
                res = self.metadata[idx].copy()
                res["score"] = round(float(similitudes[idx]), 4)
                resultados.append(res)
        
        return resultados