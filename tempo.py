import librosa

def estimate_tempo(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return tempo
