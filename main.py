from machine import Pin, SPI, I2S
import os
import sdcard

# SD module pins and SPI configuration
cs = Pin(5)
sck = Pin(18)
mosi = Pin(23)
miso = Pin(19)

spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

#  I2S configuration
bck_pin = Pin(27)
ws_pin = Pin(26)
sdout_pin = Pin(25)

audio_out = I2S(0,
                sck = bck_pin,
                ws=ws_pin,
                sd=sdout_pin,
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=44100,
                ibuf=20000)

# mount the SD card
try:
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    print("SD sucessfully mounted")
except Exception as error:
    print(f"SD Error: {error}")
    
# Wav file playback
def play_wav(filename):
    try:
        with open(filename, "rb") as wav_file:
            wav_file.seek(44)
            print(f"Playing: {filename}")
            while True:
                audio_data = wav_file.read(1024)
                if not audio_data:
                    break
                audio_out.write(audio_data)
            print("Playback finished")
    except Exception as error:
        print(f"Error: {error}")
        
# Execution
try:
    play_wav("/sd/experimento_oddball_full.wav")
finally:
    os.umount("/sd")
    print("SD Card unmounted")