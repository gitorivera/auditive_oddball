from pydub import AudioSegment, generators
import numpy as np
import random

# Función para generar un tono sinusoidal
def generar_tono(frecuencia, duracion_ms, volumen_db):
    tono = generators.Sine(frecuencia).to_audio_segment(duration=duracion_ms)
    tono = tono - (tono.dBFS - volumen_db)  # Ajustar el volumen
    return tono

# Parámetros ajustables
duracion_tono_ms = 300        # Duración de cada tono en milisegundos
intervalo_ms = 600            # Intervalo entre tonos en milisegundos
duracion_total_ms = 60000     # Duración total del experimento en milisegundos
volumen_db = -20              # Volumen en decibelios (-60 a 0 dBFS)

# Frecuencias para los tonos
frecuencia_frecuente = 500    # Frecuencia del tono frecuente en Hz
frecuencia_objetivo = 1500    # Frecuencia del tono objetivo en Hz
frecuencia_distractor = 1000  # Frecuencia del tono distractor en Hz

# Probabilidades de aparición (deben sumar 1)
probabilidad_frecuente = 0.6
probabilidad_objetivo = 0.2
probabilidad_distractor = 0.2

# Generar tonos individuales
tono_frecuente = generar_tono(frecuencia_frecuente, duracion_tono_ms, volumen_db)
tono_objetivo = generar_tono(frecuencia_objetivo, duracion_tono_ms, volumen_db)
tono_distractor = generar_tono(frecuencia_distractor, duracion_tono_ms, volumen_db)
silencio = AudioSegment.silent(duration=intervalo_ms)

# Crear la secuencia del experimento
secuencia = AudioSegment.empty()
tiempo_actual = 0

while tiempo_actual < duracion_total_ms:
    r = random.random()
    if r < probabilidad_frecuente:
        tono = tono_frecuente
    elif r < probabilidad_frecuente + probabilidad_objetivo:
        tono = tono_objetivo
    else:
        tono = tono_distractor
    secuencia += tono + silencio
    tiempo_actual += duracion_tono_ms + intervalo_ms

# Ajustar la duración total si es necesario
secuencia = secuencia[:duracion_total_ms]

# Guardar el archivo de audio
secuencia.export("experimento_oddball.wav", format="wav")
