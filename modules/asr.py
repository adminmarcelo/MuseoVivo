import speech_recognition as sr

class ASREngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Ajuste de sensibilidad al ruido ambiental
        self.recognizer.dynamic_energy_threshold = True

    def transcribir_desde_mic(self):
        """Captura audio del micrófono y lo convierte a texto."""
        with sr.Microphone() as source:
            print(">>> Escuchando... (hablá ahora)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            texto = self.recognizer.recognize_google(audio, language="es-AR")
            return texto
        except sr.UnknownValueError:
            print("No se entendió el audio.")
            return None
        except sr.RequestError as e:
            print(f"Error en el servicio ASR; {e}")
            return None

    def calcular_wer(self, referencia, hipotesis):
        """Métrica obligatoria: Word Error Rate."""
        ref = referencia.split()
        hyp = hipotesis.split()
        import numpy as np
        d = np.zeros((len(ref) + 1) * (len(hyp) + 1), dtype=np.uint8)
        d = d.reshape((len(ref) + 1, len(hyp) + 1))
        for i in range(len(ref) + 1): d[i][0] = i
        for j in range(len(hyp) + 1): d[0][j] = j
        for i in range(1, len(ref) + 1):
            for j in range(1, len(hyp) + 1):
                if ref[i-1] == hyp[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
        return float(d[len(ref)][len(hyp)]) / len(ref)

    # CORRECCIÓN AQUÍ: Este método debe estar dentro de la clase
    def transcribir_desde_archivo(self, ruta_archivo):
        """Procesa un archivo de audio (útil para Streamlit o tests)"""
        with sr.AudioFile(ruta_archivo) as source:
            audio = self.recognizer.record(source)
        try:
            # Opción principal: API de Google
            return self.recognizer.recognize_google(audio, language="es-AR")
        except:
            return None 