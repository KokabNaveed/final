import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import os

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

def plot_waveform_with_sampling_rate(file_path,filename,username):
    # Load the audio file
    audio_data, sampling_rate = load_audio(file_path)

    # Time axis for the waveform
    time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_data, label='Audio waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title(f'Audio Waveform and Sampling Rate: {sampling_rate} Hz')
    plt.grid(True)
    plt.legend()

    # Annotate the sampling rate
    plt.text(0.5, max(audio_data), f'Sampling Rate: {sampling_rate} Hz', 
             horizontalalignment='center', verticalalignment='top', fontsize=12, color='red')

    # Save the plot as an image file
    plot_filename = f"{username}_{filename}_waveform_with_sampling_rate.png"
    img_path = os.path.join('static', plot_filename)
    plt.savefig(img_path)
    plt.close()

    return img_path

def calculate_decibels_with_sampling_rate(file_path,reference_pressure=20e-6):
    # Load audio file
    audio_data, _ = load_audio(file_path)
    
    # Calculate RMS
    rms = np.sqrt(np.mean(audio_data**2))
    
    # Calculate decibels using the RMS value and reference pressure
    decibels = 20 * np.log10(rms / reference_pressure)
    
    return decibels
