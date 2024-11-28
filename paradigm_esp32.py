from machine import Pin, DAC
import time
import math
import random

# Parámetros del experimento
frequent_stimulus_freq = 500    # Estímulo frecuente
distractor_freq = 1000          # Distractor
target_freq = 1500              # Target

pulse_duration = 100         # Duración del estímulo en milisegundos
inter_stimulus_interval = 500   # Intervalo entre estímulos en milisegundos


# Configuración del pin DAC (GPIO25 o GPIO26)
dac = DAC(Pin(25))  # Canal DAC1 (GPIO25)

# Configuración del pin para triggers
trigger_pin = Pin(26, Pin.OUT)  # GPIO26 (modificar si es necesario)



def send_trigger(pulse_count):

    for _ in range(pulse_count):
        trigger_pin.on()
        time.sleep_ms(pulse_duration)
        trigger_pin.off()
        time.sleep_ms(inter_pulse_interval)