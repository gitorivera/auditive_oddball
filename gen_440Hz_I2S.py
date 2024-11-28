from machine import Pin, I2S
import math
import array
import time

# pin config
bck_pin = Pin(27)
ws_pin = Pin(26)
sdout_pin = Pin(25)

#I2S configuration
audio_out = I2S(0,
                sck=bck_pin,
                ws=ws_pin,
                sd=sdout_pin,
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=44100,
                ibuf=20000)

# sine wave parameters
sample_rate = 44100
freq = 440
amplitud = 10000
samples=100

# sine wave generation
sine_wave = array.array("h", [
    int(amplitud * math.sin(2*math.pi*freq*i/sample_rate))
    for i in range(samples)
    ])

print('tone generation')

while True:
    audio_out.write(bytes(sine_wave))


