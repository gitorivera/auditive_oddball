# Oddball Auditivo

[English](README.md) | **Español**

Estimulador auditivo *oddball* de bajo costo para obtener el potencial relacionado con eventos **P300** en experimentos de EEG. Las secuencias de estímulos se generan en un PC como archivos WAV estéreo y se reproducen con un **ESP32** con **MicroPython**, que las lee desde una tarjeta SD y emite el audio por **I2S**.

Cada archivo estéreo contiene:

- **Canal izquierdo:** los estímulos auditivos (tonos estándar, diana y distractor).
- **Canal derecho:** pulsos de sincronización (*triggers*) que codifican el tipo de estímulo, para alinear el registro de EEG con cada evento.

## Estructura del repositorio

```
auditive_oddball/
├── gen_audio_full_sync.py   # Script de PC: genera el WAV oddball estéreo (tonos + triggers)
├── Parameters.md            # Resumen del protocolo experimental
├── data/                    # Código MicroPython para el ESP32
│   ├── main.py              # Monta la tarjeta SD y reproduce un WAV por I2S
│   ├── sdcard.py            # Controlador de tarjeta SD para MicroPython (SPI)
│   └── gen_440Hz_I2S.py     # Prueba de I2S: tono senoidal continuo de 440 Hz
└── dataset/                 # Archivos de estímulos generados
    ├── experimento_oddball_estereo_sync.wav   # Secuencia estéreo de ~60 s
    ├── experimento_oddball_estereo_sync.pkf   # Archivo de picos del editor de audio
    └── oddball_short.wav                      # Secuencia estéreo de ~6 s (pruebas)
```

## Paradigma

Oddball auditivo de tres estímulos:

| Estímulo   | Frecuencia | Probabilidad | Trigger (canal derecho) |
|------------|------------|--------------|-------------------------|
| Estándar   | 2000 Hz    | 0.60         | 1 pulso                 |
| Diana      | 500 Hz     | 0.20         | 3 pulsos                |
| Distractor | 1000 Hz    | 0.20         | 2 pulsos                |

Los pulsos de sincronización son ráfagas de 10 ms de una senoidal de 1 kHz separadas por 10 ms de silencio, alineadas con el inicio de cada tono.

El protocolo experimental completo (600 estímulos, tonos de 50 ms con subida/bajada de 5 ms, 90 dB, intervalo entre estímulos aleatorio de 1.16–1.44 s, ~13 min de registro de EEG, el participante presiona un botón del ratón ante la diana) está descrito en [Parameters.md](Parameters.md).

> **Nota:** los valores actuales de `gen_audio_full_sync.py` (tonos de 300 ms, intervalo fijo de 600 ms, 6 s en total, −20 dBFS) son una configuración corta para pruebas. Modifique los parámetros al inicio del script para ajustarlos al protocolo.

## Requisitos

### PC (generación de estímulos)

- Python 3
- [pydub](https://github.com/jiaaro/pydub)
- [FFmpeg](https://ffmpeg.org/) (pydub lo usa para exportar)

```bash
pip install pydub
```

### Hardware

- Placa ESP32 con firmware MicroPython
- Módulo DAC / amplificador I2S (p. ej. MAX98357A)
- Módulo de tarjeta microSD (SPI)

Conexiones por defecto (ver `data/main.py`):

| Función        | Pin ESP32 |
|----------------|-----------|
| I2S BCLK       | GPIO 27   |
| I2S LRC (WS)   | GPIO 26   |
| I2S DIN        | GPIO 25   |
| SD CS          | GPIO 5    |
| SD SCK         | GPIO 18   |
| SD MOSI        | GPIO 23   |
| SD MISO        | GPIO 19   |

## Uso

1. **Genere el archivo de estímulos** en su PC:

   ```bash
   python gen_audio_full_sync.py
   ```

   El resultado se guarda en `dataset/oddball_short.wav` (44.1 kHz, 16 bits, estéreo).

2. **Copie el archivo WAV** a la raíz de la tarjeta microSD e insértela en el módulo SD.

3. **Cargue el código del ESP32** (`data/main.py` y `data/sdcard.py`) en la placa, por ejemplo con [Thonny](https://thonny.org/) o `mpremote`:

   ```bash
   mpremote cp data/sdcard.py data/main.py :
   ```

4. **Ajuste el nombre del archivo** en la llamada `play_wav(...)` al final de `data/main.py` para que coincida con el de la tarjeta SD y reinicie la placa. El archivo se reproduce una vez y luego se desmonta la tarjeta SD.

Para comprobar las conexiones de audio sin tarjeta SD, ejecute `data/gen_440Hz_I2S.py`, que emite un tono continuo de 440 Hz.

## Estado del proyecto

En desarrollo. Puntos pendientes conocidos:

- `data/main.py` configura el I2S en `MONO`, mientras que los archivos generados son estéreo; el formato I2S debe coincidir con el del archivo para que se emitan correctamente tanto el canal de tonos como el de triggers.
- La sincronización entre el canal de tonos y el de triggers todavía se está ajustando (ver la rama `manito-branch`).

## Autores

- Jorge Rivera (hardware)
- Manito (software)

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

`data/sdcard.py` es el controlador de tarjeta SD del proyecto [MicroPython](https://github.com/micropython/micropython-lib), también con licencia MIT.
