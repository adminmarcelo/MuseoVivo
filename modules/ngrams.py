import collections
import math
import numpy as np

class ModeloNgramas:
    def __init__(self, n=2, k=0.1):
        self.n = n  # Por defecto usamos Bigramas
        self.k = k  # Parámetro de suavizado Add-k
        self.counts = collections.defaultdict(collections.Counter)
        self.context_counts = collections.defaultdict(int)
        self.vocabulario = set()

    def entrenar(self, corpus_tokens):
        """Entrena el modelo a partir de los tokens del corpus."""
        for i in range(len(corpus_tokens) - self.n + 1):
            contexto = tuple(corpus_tokens[i:i+self.n-1])
            siguiente = corpus_tokens[i+self.n-1]
            self.counts[contexto][siguiente] += 1
            self.context_counts[contexto] += 1
            self.vocabulario.add(siguiente)
        print(f"✅ Modelo de {self.n}-gramas entrenado con {len(self.vocabulario)} palabras únicas.")

    def obtener_probabilidad(self, palabra, contexto):
        """Calcula P(w|contexto) con suavizado Add-k."""
        contexto = tuple(contexto)
        count_secuencia = self.counts[contexto][palabra]
        count_contexto = self.context_counts[contexto]
        
        # Fórmula: (count + k) / (total_contexto + k * tamaño_vocabulario)
        prob = (count_secuencia + self.k) / (count_contexto + self.k * len(self.vocabulario))
        return prob

    def calcular_perplejidad(self, texto_tokens):
        """Mide qué tan coherente es el texto para el modelo."""
        if not texto_tokens: return float('inf')
        
        log_prob_total = 0
        for i in range(len(texto_tokens) - self.n + 1):
            contexto = texto_tokens[i:i+self.n-1]
            palabra = texto_tokens[i+self.n-1]
            prob = self.obtener_probabilidad(palabra, contexto)
            log_prob_total += math.log2(prob)
        
        # Perplejidad = 2 ^ (-promedio_log_prob)
        avg_log_prob = log_prob_total / len(texto_tokens)
        return math.pow(2, -avg_log_prob)

    def predecir_siguiente(self, contexto, top_n=5):
        """Sugiere las siguientes palabras más probables."""
        contexto = tuple(contexto[-(self.n-1):])
        if contexto not in self.counts:
            return []
        
        predicciones = self.counts[contexto].most_common(top_n)
        total = self.context_counts[contexto]
        return [{"palabra": p, "prob": round(c/total, 4)} for p, c in predicciones]

    def validar_coherencia(self, texto_tokens, umbral=150.0):
        """Detecta si la consulta es 'ruido' o fuera de dominio."""
        pp = self.calcular_perplejidad(texto_tokens)
        # Una PP muy alta indica que el modelo no reconoce la secuencia
        return {"es_coherente": pp < umbral, "perplejidad": round(pp, 2)}