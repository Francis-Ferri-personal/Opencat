import os
import pyaudio
import vosk
import json
from datetime import datetime
import time  # Importamos time para medir tiempos

# Carga del modelo de Vosk
model = vosk.Model("models\\vosk-model-small-en")  # Asegúrate de poner la ruta al modelo

# Configuración del audio (formato de 16 bits, mono, 16000 Hz)
sample_rate = 16000
chunk_size = 512
channels = 1

# Inicialización de PyAudio
p = pyaudio.PyAudio()

# Abrir el flujo de entrada de audio
stream = p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size)

# Establecer el modelo de reconocimiento
rec = vosk.KaldiRecognizer(model, sample_rate)

# Función para imprimir con tiempo
def print_with_time(message):
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Formato HH:MM:SS.mmm
    print(f"[{current_time}] {message}")

def listen_for_activation_word():
    print_with_time("Escuchando...")
    while True:
        start_time = time.time()  # Inicio del cronómetro total

        # Captura del audio
        data = stream.read(chunk_size)

        
        result_partial = rec.PartialResult()
        result_partial_json = json.loads(result_partial)
        print(result_partial_json)


        # Detectar la palabra de activación
        if "alexa" in result_json.get('text', '').lower():
            print_with_time("¡Palabra de activación detectada!")
            break

        # Procesamiento del chunk de audio
        if rec.AcceptWaveform(data):
            total_time = (time.time() - start_time) * 1000  # Tiempo total en milisegundos
            result = rec.Result()
            result_json = json.loads(result)
            print_with_time(f"Resultado: {result_json} (Tiempo total: {total_time:.2f} ms)")
            
            # Detectar la palabra de activación
            if "alexa" in result_json.get('text', '').lower():
                print_with_time("¡Palabra de activación detectada!")
                break
            

# Llamar a la función para escuchar la palabra de activación
listen_for_activation_word()
