import sqlite3
import os

class BaseDatos:
    def __init__(self, db_path="data/database.sqlite"):
        self.db_path = db_path
        self.conectar()
        self.crear_tablas()

    def conectar(self):
        """Establece la conexión con el archivo SQLite."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def crear_tablas(self):
        """Crea las 3 tablas obligatorias según los requisitos del proyecto."""
        # 1. Tabla de Conocimiento: Almacena los textos del corpus [cite: 55, 261]
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conocimiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                contenido TEXT,
                fuente TEXT,
                fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Tabla de Historial: Registra cada interacción con el turista [cite: 57, 261]
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                texto_transcripto TEXT,
                respuesta_sistema TEXT,
                perplejidad REAL,
                wer REAL,
                tiempo_ms INTEGER
            )
        ''')
        
        # 3. Tabla de Métricas: Datos agregados para el Dashboard [cite: 55, 261]
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metricas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE UNIQUE,
                total_consultas INTEGER DEFAULT 0,
                wer_promedio REAL DEFAULT 0,
                pp_promedio REAL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def insertar_documento(self, titulo, contenido, fuente):
        """Inserta un nuevo fragmento de historia en la base de datos."""
        self.cursor.execute(
            "INSERT INTO conocimiento (titulo, contenido, fuente) VALUES (?, ?, ?)",
            (titulo, contenido, fuente)
        )
        self.conn.commit()

    def cerrar(self):
        self.conn.close()