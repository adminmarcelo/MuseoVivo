import streamlit as st
import time
import os
from modules.asr import ASREngine
from modules.nlp import NLPProcessor
from modules.ngrams import ModeloNgramas
from modules.search import MotorBusqueda
from modules.tts import TTSEngine
from modules.db import BaseDatos

# 1. Configuración de la Interfaz (Fase 3 de la Hoja de Ruta)
st.set_page_config(page_title="MuseoVivo Chascomús", page_icon="🏛️", layout="wide")

# Inicialización persistente de los módulos
@st.cache_resource
def inicializar_modulos():
    return ASREngine(), NLPProcessor(), ModeloNgramas(), MotorBusqueda(), TTSEngine(), BaseDatos()

asr, nlp, ngrams, search, tts, db = inicializar_modulos()

# --- BARRA LATERAL: Estado y Métricas ---
st.sidebar.title("📊 Estado del Sistema")
st.sidebar.success("Base de Datos: 33 archivos indexados")
st.sidebar.metric("Perplejidad Objetivo", "6.69")

# --- CUERPO PRINCIPAL ---
st.title("🏛️ MuseoVivo: Guía de Patrimonio")
st.markdown("Interactuá con la historia de Chascomús a través de tu voz.")

# 2. CAPTURA DE AUDIO (Bloque 4 - Web)
audio_value = st.audio_input("Presioná el micrófono para preguntar")

if audio_value:
    # Guardamos el audio temporalmente para procesarlo
    audio_path = "temp_query.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_value.read())
    
    # Iniciamos el pipeline de procesamiento
    with st.status("Procesando consulta...", expanded=True) as status:
        start_time = time.time()
        
        # A. ASR (Voz a Texto usando el archivo guardado)
        st.write("🎙️ Transcribiendo audio...")
        texto_usuario = asr.transcribir_desde_archivo(audio_path)
        
        if texto_usuario:
            st.chat_message("user").write(texto_usuario)
            
            # B. NLP & BÚSQUEDA (Bloques 1 y 3)
            st.write("🔍 Buscando en el patrimonio...")
            entidades = nlp.extraer_entidades(texto_usuario)
            resultado, score = search.buscar_mas_relevante(texto_usuario)
            
            # C. VALIDACIÓN (Bloque 2)
            pp = ngrams.calcular_perplejidad(texto_usuario)
            
            # D. RESULTADOS Y TTS (Bloque 4)
            st.write("🔊 Generando respuesta...")
            if score > 0.3: # Umbral de similitud configurado
                respuesta_texto = resultado['contenido']
                st.chat_message("assistant").write(respuesta_texto)
                
                # Generamos y mostramos el audio de respuesta
                path_audio_res = tts.sintetizar_para_web(respuesta_texto)
                st.audio(path_audio_res)
            else:
                st.warning("No encontré información específica en el corpus histórico.")
            
            # E. PERSISTENCIA (Bloque 6)
            tiempo_resp = time.time() - start_time
            db.guardar_interaccion(texto_usuario, score, pp, tiempo_resp)
            
            status.update(label="Procesamiento completado", state="complete")
        else:
            st.error("No se pudo procesar el audio. Por favor, intentá de nuevo.") 