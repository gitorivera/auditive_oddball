from machine import Pin, I2S
import math
import array
import time

# Configuración de pines
bck_pin = Pin(27)  # Pin de reloj (BCLK)
ws_pin = Pin(26)   # Pin de selección de palabra (LRC)
sd_pin = Pin(25)   # Pin de datos (DIN)

# Configuración de I2S
audio_out = I2S(0,                          # Canal I2S 0
                sck=bck_pin,                # Reloj (BCLK)
                ws=ws_pin,                  # Selección de palabra (LRC)
                sd=sd_pin,                  # Datos (DIN)
                mode=I2S.TX,                # Solo transmisión
                bits=16,                    # Resolución de audio en bits
                format=I2S.MONO,            # Formato mono
                rate=44100,                 # Frecuencia de muestreo
                ibuf=20000)                 # Tamaño del buffer

# Generación de una onda seno de 440 Hz
sample_rate = 44100                         # Frecuencia de muestreo (Hz)
freq = 440                                  # Frecuencia del tono (Hz)
amplitude = 5000                           # Amplitud máxima para 16 bits
samples = 100                               # Número de muestras por ciclo

# Generar los valores de la onda seno
sine_wave = array.array("h", [
    int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
    for i in range(samples)
])

# Reproducción continua
print("Generación de tono de 440 Hz...")
while True:
    audio_out.write(bytes(sine_wave))  # Enviar datos al periférico I2S


