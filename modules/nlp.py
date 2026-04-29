import spacy
from spacy.matcher import PhraseMatcher

class NLPProcessor:
    def __init__(self):
        # Cargamos el modelo oficial en español [cite: 200]
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except OSError:
            import os
            os.system("python -m spacy download es_core_news_sm")
            self.nlp = spacy.load("es_core_news_sm")
        
        # Diccionario de intenciones para clasificar la consulta [cite: 37]
        self.intenciones = {
            "historia": ["cuéntame", "historia", "pasó", "quién", "fundó", "origen"],
            "ubicación": ["dónde", "queda", "llegar", "ubicación", "dirección"],
            "información": ["qué es", "precio", "entrada", "horario", "abierto"]
        }

    def extraer_entidades_personalizadas(self, doc):
        """Reconocimiento de entidades expandido (NER)[cite: 35]."""
        entidades = []
        for ent in doc.ents:
            # Mapeamos etiquetas de spaCy a etiquetas del dominio MuseoVivo
            label = ent.label_
            if label == "LOC": label = "MONUMENTO_LUGAR"
            if label == "PER": label = "PERSONAJE_HISTORICO"
            if label == "DATE": label = "EPOCA_FECHA"
            entidades.append({"texto": ent.text, "tipo": label})
        
        # Aquí podrías sumar reglas (RegEx) para entidades específicas de Chascomús
        return entidades

    def detectar_intencion(self, texto):
        """Clasificación del tipo de consulta del usuario[cite: 37]."""
        texto_norm = texto.lower()
        for intencion, palabras in self.intenciones.items():
            if any(p in texto_norm for p in palabras):
                return intencion
        return "general"

    def procesar_consulta(self, texto):
        """Pipeline completo del Bloque 1: Tokenización -> POS -> NER -> Intención[cite: 33]."""
        doc = self.nlp(texto)
        
        # Tokenización y POS Tagging (priorizando sustantivos y adjetivos) [cite: 34, 36]
        analisis = [
            {
                "token": t.text,
                "lemma": t.lemma_.lower(),
                "pos": t.pos_,
                "es_stop": t.is_stop
            }
            for t in doc
        ]
        
        # Limpieza para el motor de búsqueda (solo lemas relevantes)
        tokens_limpios = [t.lemma_.lower() for t in doc if not t.is_stop and not t.is_punct]

        return {
            "texto_original": texto,
            "tokens_limpios": tokens_limpios,
            "analisis_pos": analisis,
            "entidades": self.extraer_entidades_personalizadas(doc),
            "intencion": self.detectar_intencion(texto)
        }