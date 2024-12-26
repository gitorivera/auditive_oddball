from pydub import AudioSegment, generators
import random

# Función para generar un tono sinusoidal
def generar_tono(frecuencia, duracion_ms, volumen_db):
    tono = generators.Sine(frecuencia).to_audio_segment(duration=duracion_ms)
    tono = tono - (tono.dBFS - volumen_db)  # Ajustar el volumen
    return tono.set_frame_rate(44100).set_sample_width(2).set_channels(1)  # Ajustes técnicos

# Función para generar pulsos de sincronización
def generar_pulsos(num_pulsos, duracion_pulso_ms, duracion_total_ms, sincronizacion_padding_ms=0):
    # Crear un silencio inicial para sincronizar con el inicio del tono
    pulso = AudioSegment.silent(duration=sincronizacion_padding_ms)
    for _ in range(num_pulsos):
        # Usar generators para crear el pulso sinusoidal
        pulso_sinusoidal = generators.Sine(1000).to_audio_segment(duration=duracion_pulso_ms).set_sample_width(2).set_frame_rate(44100).set_channels(1)
        pulso += pulso_sinusoidal
        pulso += AudioSegment.silent(duration=duracion_pulso_ms)  # Silencio entre pulsos
    # Completar con silencio hasta la duración total
    pulso += AudioSegment.silent(duration=duracion_total_ms - len(pulso))
    return pulso

# Parámetros
duracion_tono_ms = 300  # Duración de cada tono en milisegundos
intervalo_ms = 600  # Intervalo entre tonos en milisegundos
duracion_total_ms = 6000  # Duración total del experimento en milisegundos
volumen_db = -20  # Volumen de los tonos en decibelios

frecuencia_frecuente = 2000    # Frecuencia del tono frecuente
frecuencia_objetivo = 500    # Frecuencia del tono objetivo
frecuencia_distractor = 1000  # Frecuencia del tono distractor

probabilidad_frecuente = 0.6
probabilidad_objetivo = 0.2
probabilidad_distractor = 0.2

duracion_pulso_ms = 10  # Duración de cada pulso de sincronización
sincronizacion_padding_ms = 0  # Ajuste de sincronización entre tono y trigger

# Generar tonos
tono_frecuente = generar_tono(frecuencia_frecuente, duracion_tono_ms, volumen_db)
tono_objetivo = generar_tono(frecuencia_objetivo, duracion_tono_ms, volumen_db)
tono_distractor = generar_tono(frecuencia_distractor, duracion_tono_ms, volumen_db)

# Crear las secuencias izquierda (tonos) y derecha (triggers)
secuencia_izquierda = AudioSegment.empty()
secuencia_derecha = AudioSegment.empty()

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
    pulsos = generar_pulsos(num_pulsos, duracion_pulso_ms, duracion_tono_ms, sincronizacion_padding_ms)

    # Añadir tono al canal izquierdo
    secuencia_izquierda += tono + AudioSegment.silent(duration=intervalo_ms)

    # Añadir pulsos sincronizados al canal derecho
    secuencia_derecha += pulsos + AudioSegment.silent(duration=intervalo_ms)

    tiempo_actual += duracion_tono_ms + intervalo_ms

# Ajustar duración total
secuencia_izquierda = secuencia_izquierda[:duracion_total_ms]
secuencia_derecha = secuencia_derecha[:duracion_total_ms]

# Combinar los canales en estéreo
secuencia_estereo = AudioSegment.from_mono_audiosegments(secuencia_izquierda, secuencia_derecha)



# Exportar el archivo estéreo
secuencia_estereo.export("dataset/oddball_short.wav", format="wav", parameters=["-ar", "44100", "-ac", "2", "-sample_fmt", "s16"])