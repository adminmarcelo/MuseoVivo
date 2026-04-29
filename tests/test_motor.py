import sys
import os

# Agregamos la carpeta raíz al camino de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from modules.db import BaseDatos
from modules.nlp import NLPProcessor
from modules.search import MotorBusqueda

# 1. Inicializar
db = BaseDatos()
nlp = NLPProcessor()
motor = MotorBusqueda()

# 2. Cargar conocimiento en el motor
motor.entrenar_con_db(db)

# 3. Simular pregunta de turista
pregunta = "Contame la historia de la catedral de Chascomús y quién la fundó."
print(f"\nTurista dice: {pregunta}")

# 4. Procesar con NLP (Bloque 1)
procesado = nlp.procesar_consulta(pregunta)
print(f"Intención: {procesado['intencion']}")
print(f"Entidades: {procesado['entidades']}")

# 5. Buscar (Bloque 3)
resultados = motor.buscar(procesado['tokens_limpios'])

if resultados:
    print(f"\nGuía dice: {resultados[0]['contenido'][:200]}...")
    print(f"(Fuente: {resultados[0]['fuente']} | Score: {resultados[0]['score']})")
else:
    print("\nGuía dice: Perdón, no encontré información sobre eso.")