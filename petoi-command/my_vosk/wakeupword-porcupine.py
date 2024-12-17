import pvporcupine
import pyaudio
import numpy as np

# Configura tu palabra clave y el modelo adecuado
keyword_file = "path_to_wakeup.ppn"  # Ruta al archivo del modelo de la palabra clave

# Inicializa Porcupine con la palabra clave
porcupine = pvporcupine.create(
  access_key='d5Mb1XXmtlM19CUycfk/GRnhGKpbgVEwfAqyOyfY16I36ehTdMgldg==',
  keyword_paths=['perrito_es_windows_v3_0_0.ppn'],
  model_path='porcupine_params_es.pv'
)


# Inicializa PyAudio
p = pyaudio.PyAudio()

# Abre el flujo de audio
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=porcupine.sample_rate,
                input=True,
                frames_per_buffer=porcupine.frame_length)

print("Esperando la palabra clave...")

try:
    while True:
        # Lee el audio del micrófono
        pcm = np.frombuffer(stream.read(porcupine.frame_length), dtype=np.int16)

        # Pasa el audio a Porcupine
        result = porcupine.process(pcm)

        # Si se detecta la palabra clave
        if result >= 0:
            print("¡Palabra clave detectada!")

except KeyboardInterrupt:
    print("Detenido por el usuario")

finally:
    # Cierra el flujo de audio y Porcupine
    stream.stop_stream()
    stream.close()
    p.terminate()
    porcupine.delete()
