# Bitrate.py

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

def get_bitrate(file_path):
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
            bitrate = audio.info.bitrate
        elif file_path.lower().endswith('.wav'):
            audio = WAVE(file_path)
            # For WAV files, we need to calculate the bitrate
            bitrate = audio.info.sample_rate * audio.info.bits_per_sample * audio.info.channels
        else:
            raise ValueError('Unsupported file format')
        
        return bitrate
    except Exception as e:
        print(f"Error: {e}")
        return None
