import requests
import base64
from pydub import AudioSegment
from pydub.playback import play
import io
import pyttsx3
import os

def text_to_speech_stream(text):
    api_key = "AIzaSyC17dnNbnSO6WRa6ZNgwJDgfrCSUThqidc"
    # Google Text-to-Speech API endpoint
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    # İstek verisi (JSON formatında)
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",  # Türkçe dil kodu
            "ssmlGender": "MALE"  # Erkek sesi
        },
        "audioConfig": {
            "audioEncoding": "MP3",  # Çıkış formatı MP3
            "speakingRate": 1  # Konuşma hızı
        }
    }

    # Send post request to api
    response = requests.post(url, json=data)

    # Check the response
    if response.status_code == 200:
        # Get the voice
        audio_content = response.json().get("audioContent")

        if audio_content:

            audio_data = base64.b64decode(audio_content)


            audio_stream = io.BytesIO(audio_data)


            sound = AudioSegment.from_file(audio_stream, format="mp3")
            play(sound)
        else:
            print("Error:")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)






# def text_to_speech_local(text):
#     # Inicializa el motor de texto a voz
#     engine = pyttsx3.init()

#     # Configura las propiedades del motor (idioma, velocidad, voz, etc.)
#     engine.setProperty('rate', 150)  # Velocidad de habla
#     engine.setProperty('volume', 1)  # Volumen (1.0 es el máximo)
    
#     # Obtiene las voces disponibles y selecciona una
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         if 'en_US' in voice.id:  # Selecciona una voz en inglés estadounidense
#             engine.setProperty('voice', voice.id)
#             break
    
#     # Convierte el texto a voz
#     engine.say(text)
    
#     # Procesa y reproduce el audio
#     engine.runAndWait()

def text_to_speech_local(text):
    # Inicializa el motor de texto a voz
    engine = pyttsx3.init()

    # Configura las propiedades del motor (velocidad y volumen)
    engine.setProperty('rate', 150)  # Velocidad de habla
    engine.setProperty('volume', 1)  # Volumen (1.0 es el máximo)
    
    # Obtiene el idioma de la variable de entorno LANGUAGE
    language = os.getenv('LANGUAGE', 'en')  # Valor predeterminado: inglés
    
    # Obtiene las voces disponibles
    voices = engine.getProperty('voices')
    selected_voice = None

    # Selecciona una voz en función del idioma
    for voice in voices:
        if language == 'en' and 'en_US' in voice.id:  # Voz en inglés
            selected_voice = voice.id
            break
        elif language == 'sp' and 'es_' in voice.id:  # Voz en español
            selected_voice = voice.id
            break

    # Configura la voz seleccionada si se encuentra
    if selected_voice:
        engine.setProperty('voice', selected_voice)
    else:
        print("No se encontró una voz adecuada para el idioma seleccionado.")
    
    # Convierte el texto a voz
    engine.say(text)
    
    # Procesa y reproduce el audio
    engine.runAndWait()