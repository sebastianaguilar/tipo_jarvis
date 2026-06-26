# Jarvis (Primer prototipo)

Este repositorio contiene uno de mis primeros experimentos para crear un asistente de voz tipo **Jarvis** en macOS.

La arquitectura estaba dividida en tres archivos.

## Archivos

### vision.py

Es el cerebro del sistema.

Funciones:

- Escucha el micrófono mientras mantengo presionada la barra espaciadora.
- Transcribe la voz usando **Whisper**.
- Envía el texto a **OpenAI**.
- Convierte la respuesta a voz con **ElevenLabs**.
- Reproduce automáticamente la respuesta.

---

### VideoJar.pde

Sketch de **Processing**.

Su única función era mostrar una animación de Jarvis a pantalla completa (`jar.mp4`) mientras el asistente estaba ejecutándose.

En esta versión **no existe comunicación** entre Python y Processing; simplemente reproduce el video en bucle.

---

### jarvis.scpt

Script de **AppleScript** para iniciar todo automáticamente.

Hace lo siguiente:

1. Abre Terminal.
2. Entra a la carpeta del proyecto.
3. Ejecuta `vision.py`.
4. Activa la aplicación `VideoJar` (Processing).

De esta forma todo inicia con un solo clic.

---

## Arquitectura

```
               jarvis.scpt
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
  vision.py               VideoJar.pde
        │                       │
        ▼                       │
 Micrófono                      │
        ▼                       │
 Whisper                        │
        ▼                       │
 OpenAI                         │
        ▼                       │
 ElevenLabs                     │
        ▼                       │
 Audio                    Video en loop
```

---

## Estado del proyecto

Este fue un prototipo inicial.

Más adelante la idea era que `vision.py` pudiera comunicarse con Processing para cambiar las animaciones según el estado del asistente:

- Escuchando
- Pensando
- Hablando
- Esperando

pero esa parte nunca se implementó en esta versión.

Este repositorio se conserva únicamente como respaldo histórico del proyecto.
