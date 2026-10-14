# Auditory Oddball

**English** | [Español](README.es.md)

A low-cost auditory *oddball* stimulator for eliciting the **P300** event-related potential in EEG experiments. Stimulus sequences are generated on a PC as stereo WAV files and played back by an **ESP32** running **MicroPython**, reading from an SD card and outputting audio over **I2S**.

Each stereo file carries:

- **Left channel:** the auditory stimuli (standard, target and distractor tones).
- **Right channel:** synchronization trigger pulses that encode the stimulus type, so the EEG recording can be aligned with each event.

## Repository structure

```
auditive_oddball/
├── gen_audio_full_sync.py   # PC script: generates the stereo oddball WAV (tones + triggers)
├── Parameters.md            # Summary of the experimental protocol (Spanish)
├── data/                    # MicroPython code for the ESP32
│   ├── main.py              # Mounts the SD card and plays a WAV file over I2S
│   ├── sdcard.py            # MicroPython SD-card driver (SPI)
│   └── gen_440Hz_I2S.py     # I2S test: continuous 440 Hz sine tone
└── dataset/                 # Generated stimulus files
    ├── experimento_oddball_estereo_sync.wav   # ~60 s stereo sequence
    ├── experimento_oddball_estereo_sync.pkf   # Audio editor peak file
    └── oddball_short.wav                      # ~6 s stereo sequence (testing)
```

## Paradigm

Three-stimulus auditory oddball:

| Stimulus   | Frequency | Probability | Trigger (right channel) |
|------------|-----------|-------------|-------------------------|
| Standard   | 2000 Hz   | 0.60        | 1 pulse                 |
| Target     | 500 Hz    | 0.20        | 3 pulses                |
| Distractor | 1000 Hz   | 0.20        | 2 pulses                |

Trigger pulses are 10 ms bursts of a 1 kHz sine separated by 10 ms of silence, aligned with the start of each tone.

The full experimental protocol (600 stimuli, 50 ms tones with 5 ms rise/fall, 90 dB, random inter-stimulus interval of 1.16–1.44 s, ~13 min of EEG recording, participant presses a mouse button on targets) is described in [Parameters.md](Parameters.md).

> **Note:** the current defaults in `gen_audio_full_sync.py` (300 ms tones, fixed 600 ms interval, 6 s total, −20 dBFS) are short settings for testing. Edit the parameters at the top of the script to match the protocol.

## Requirements

### PC (stimulus generation)

- Python 3
- [pydub](https://github.com/jiaaro/pydub)
- [FFmpeg](https://ffmpeg.org/) (used by pydub to export)

```bash
pip install pydub
```

### Hardware

- ESP32 board with MicroPython firmware
- I2S DAC / amplifier module (e.g. MAX98357A)
- microSD card module (SPI)

Default pin mapping (see `data/main.py`):

| Function       | ESP32 pin |
|----------------|-----------|
| I2S BCLK       | GPIO 27   |
| I2S LRC (WS)   | GPIO 26   |
| I2S DIN        | GPIO 25   |
| SD CS          | GPIO 5    |
| SD SCK         | GPIO 18   |
| SD MOSI        | GPIO 23   |
| SD MISO        | GPIO 19   |

## Usage

1. **Generate the stimulus file** on your PC:

   ```bash
   python gen_audio_full_sync.py
   ```

   The output is written to `dataset/oddball_short.wav` (44.1 kHz, 16-bit, stereo).

2. **Copy the WAV file** to the root of the microSD card and insert it in the SD module.

3. **Upload the ESP32 code** (`data/main.py` and `data/sdcard.py`) to the board, e.g. with [Thonny](https://thonny.org/) or `mpremote`:

   ```bash
   mpremote cp data/sdcard.py data/main.py :
   ```

4. **Set the file name** in the `play_wav(...)` call at the end of `data/main.py` so it matches the file on the SD card, then reset the board. The file is played once and the SD card is unmounted.

To check the audio wiring without an SD card, run `data/gen_440Hz_I2S.py`, which outputs a continuous 440 Hz tone.

## Project status

Work in progress. Known open points:

- `data/main.py` sets up I2S as `MONO`, while the generated files are stereo; the I2S format has to match the file for both the tone and trigger channels to be output correctly.
- Synchronization between the tone and trigger channels is still being refined (see the `manito-branch` branch).

## Authors

- Jorge Rivera (hardware)
- Manito (software)

## License

This project is released under the [MIT License](LICENSE).

`data/sdcard.py` is the SD-card driver from the [MicroPython](https://github.com/micropython/micropython-lib) project, also MIT-licensed.
