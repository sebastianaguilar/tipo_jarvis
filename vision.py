import whisper
import pyaudio
import wave
import os
import openai
import requests
import threading
import ssl
from pynput import keyboard

# Desactiva verificación de certificados en Mac si es necesario
ssl._create_default_https_context = ssl._create_unverified_context

# Claves API
openai.api_key = "sk-proj--qR5oqs-"
elevenlabs_api_key = ""
elevenlabs_voice_id = ""

# Introducción de GPT
messages = [{"role": "system", "content": "Eres un asistente inteligente y tu nombre es Jarvis. Debes hablarme de usted siempre y decirme señor sebastian. Estás integrado dentro de una aplicación, que convierte mi voz a texto, por lo tanto tu recibes mi voz convertida a texto, tu lees texto, y cuando respondes en texto, otro script convierte ese texto a voz. Por lo tanto estamos hablando."}]

# Parámetros de audio
RATE = 16000
CHUNK = 1024
TRIGGER_WORDS = ["vision", "jarvis", "yarvis", "visión", "carbis", "járbiz", "javier", "jervis", "yarvices"]

# Inicializa Whisper y PyAudio
model = whisper.load_model("base")
p = pyaudio.PyAudio()
grabando = False
frames = []

def iniciar_stream():
    return p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

def grabar_mientras_presionado():
    global grabando, frames
    grabando = True
    frames = []
    stream = iniciar_stream()
    print("🎙️ Grabando... (mantén presionada la barra espaciadora)")
    while grabando:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    guardar_y_procesar()

def guardar_y_procesar():
    filename = "temp.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    texto = transcribir_audio(filename)
    print("🗣️ Dijiste:", texto)

    respuesta = consulta_gpt(texto)
    print("🤖 Vision:", respuesta)
    texto_a_voz(respuesta)


def transcribir_audio(audio_file):
    result = model.transcribe(audio_file, fp16=False, language="es")
    return result["text"].lower()

def consulta_gpt(mensaje):
    messages.append({"role": "user", "content": mensaje})
    chat = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return chat.choices[0].message.content

def texto_a_voz(texto):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice_id}"
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }
    body = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        with open("respuesta.mp3", "wb") as f:
            f.write(response.content)
        os.system("afplay respuesta.mp3")  # Mac
    else:
        print("❌ Error en ElevenLabs:", response.text)

# Control del teclado
def on_press(key):
    if key == keyboard.Key.space and not grabando:
        threading.Thread(target=grabar_mientras_presionado).start()

def on_release(key):
    global grabando
    if key == keyboard.Key.space:
        grabando = False
bienvenida = "Buenas tardes, señor Sebastián. Soy Jarvis y estoy listo para asistirle."
print("🤖 Jarvis:", bienvenida)
texto_a_voz(bienvenida)
print("🔁 Esperando que mantengas presionada la barra espaciadora para hablar...")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

