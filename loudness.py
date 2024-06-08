import librosa
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def get_loudness(file_path):
    y, sr = librosa.load(file_path)
    # y: audio time series, sr: sampling rate
    S = np.abs(librosa.stft(y))
    # S: short-time Fourier transform of y 
    # which is a complex-valued matrix representing the frequency content of the signal 
    loudness = librosa.amplitude_to_db(S, ref=np.max)
    # magnitude spectrogram S is converted to dB-scaled spectrogram
    return loudness, sr

def plot_loudness(file_path,filename,username):
    loudness, sr = get_loudness(file_path)

    plt.figure(figsize=(10, 6))
    plt.imshow(loudness, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Loudness Heatmap')
    plt.xlabel('Time')
    plt.ylabel('Frequency (Hz)')
    plot_filename = f"{username}_{filename}_loudness_plot.png"
    output_path = os.path.join('static', plot_filename)
    plt.savefig(output_path)
    plt.close()
    return output_path
