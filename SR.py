import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

def plot_waveform_with_sampling_rate(file_path):
    # Load the audio file
    audio_data, sampling_rate = load_audio(file_path)

    # Time axis for the waveform
    time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

    # Plot the waveform
    plt.figure(figsize=(14, 6))
    plt.plot(time, audio_data, label='Audio waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title(f'Audio Waveform and Sampling Rate: {sampling_rate} Hz')
    plt.grid(True)
    plt.legend()

    # Annotate the sampling rate
    plt.text(0.5, max(audio_data), f'Sampling Rate: {sampling_rate} Hz', 
             horizontalalignment='center', verticalalignment='top', fontsize=12, color='red')

    output_path = 'static/waveform_with_sampling_rate.png'
    plt.savefig(output_path)
    plt.close()
    return output_path
