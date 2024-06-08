import librosa
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def plot_frequency_spectrum(file_path,filename,username):
    # Load audio file
    y, sr = librosa.load(file_path)

    # Compute Short-Time Fourier Transform (STFT)
    D = librosa.stft(y)

    # Compute the magnitude spectrum
    magnitude = np.abs(D)

    # Convert magnitude to decibels
    magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max)

    # Plot the frequency spectrum
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(magnitude_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Frequency Spectrum')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plot_filename = f"{username}_{filename}_plot_path_sr.png"
    output_path = os.path.join('static', plot_filename)
    plt.savefig(output_path)
    plt.close()
    return output_path
