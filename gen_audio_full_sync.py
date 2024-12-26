from pydub import AudioSegment, generators
import random
import os

# Crear un directorio para almacenar los archivos de Audio
os.makedirs("dataset", exist_ok=True)


# Función para generar un tono sinusoidal


def generar_tono(frecuencia, duracion_ms, volumen_db):
    tono = generators.Sine(frecuencia).to_audio_segment(duration=duracion_ms)
    tono = tono - (tono.dBFS - volumen_db)  # Ajustar el volumen
    # Ajustes técnicos
    return tono.set_frame_rate(44100).set_sample_width(2).set_channels(1)

# Función para generar pulsos de sincronización


def generar_pulsos(num_pulsos, duracion_pulso_ms, duracion_total_ms):
    # Crear un silencio inicial para sincronizar con el inicio del tono
    pulso = AudioSegment.silent(duration=0)
    for _ in range(num_pulsos):
        # Usar generators para crear el pulso sinusoidal
        pulso_sinusoidal = generators.Square(1000).to_audio_segment(
            duration=duracion_pulso_ms
        ).set_sample_width(2).set_frame_rate(44100).set_channels(1)

        pulso += pulso_sinusoidal
        # Silencio entre pulsos
        pulso += AudioSegment.silent(duration=duracion_pulso_ms)
    # Completar con silencio hasta la duración total
    if len(pulso) < duracion_total_ms:
        pulso += AudioSegment.silent(duration=duracion_total_ms - len(pulso))
    return pulso[:duracion_total_ms]


# Parámetros
duracion_tono_ms = 300  # Duración de cada tono en milisegundos
intervalo_ms = 600  # Intervalo entre tonos en milisegundos
duracion_total_ms = 60000  # Duración total del experimento en milisegundos
volumen_db = -20  # Volumen de los tonos en decibelios

frecuencia_frecuente = 500    # Frecuencia del tono frecuente
frecuencia_objetivo = 1500    # Frecuencia del tono objetivo
frecuencia_distractor = 1000  # Frecuencia del tono distractor

probabilidad_frecuente = 0.6
probabilidad_objetivo = 0.2
probabilidad_distractor = 0.2

duracion_pulso_ms = 10  # Duración de cada pulso de sincronización

# Generar tonos
tono_frecuente = generar_tono(
    frecuencia_frecuente, duracion_tono_ms, volumen_db)
tono_objetivo = generar_tono(
    frecuencia_objetivo, duracion_tono_ms, volumen_db)
tono_distractor = generar_tono(
    frecuencia_distractor, duracion_tono_ms, volumen_db)

# Crear las secuencias izquierda (tonos) y derecha (triggers)
secuencia_izquierda = AudioSegment.silent(duration=0)
secuencia_derecha = AudioSegment.silent(duration=0)

tiempo_actual = 0

while tiempo_actual < duracion_total_ms:
    r = random.random()
    if r < probabilidad_frecuente:
        tono = tono_frecuente
        num_pulsos = 1  # Un pulso para el tono frecuente
    elif r < probabilidad_frecuente + probabilidad_objetivo:
        tono = tono_objetivo
        num_pulsos = 3  # Tres pulsos para el tono objetivo
    else:
        tono = tono_distractor
        num_pulsos = 2  # Dos pulsos para el tono distractor

    # Generar pulsos y añadirlos al canal derecho
    pulsos = generar_pulsos(num_pulsos, duracion_pulso_ms, duracion_tono_ms)

    # Añadir tono al canal izquierdo
    secuencia_izquierda += tono + AudioSegment.silent(duration=intervalo_ms)

    # Añadir pulsos sincronizados al canal derecho
    secuencia_derecha += pulsos + AudioSegment.silent(duration=intervalo_ms)

    tiempo_actual += duracion_tono_ms + intervalo_ms

# Ajustar duración total
secuencia_izquierda = secuencia_izquierda[:duracion_total_ms]
secuencia_derecha = secuencia_derecha[:duracion_total_ms]

# Reducir la amplitud del canal izquierdo

secuencia_derecha = secuencia_derecha - 10

# Combinar los canales en estéreo
secuencia_estereo = AudioSegment.from_mono_audiosegments(
    secuencia_izquierda, secuencia_derecha
)


# Exportar el archivo estéreo
secuencia_estereo.export("dataset/experimento_oddball_estereo_sync.wav",
                         format="wav",
                         parameters=[
                             "-ar",
                             "44100",
                             "-ac",
                             "2",
                             "-sample_fmt",
                             "s16"
                         ]
                         )
