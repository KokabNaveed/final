import librosa
import numpy as np
import matplotlib.pyplot as plt

def plot_waveform_with_peak(file_path):
    # Load audio file
    y, sr = librosa.load(file_path)

    # Calculate time array
    t = np.arange(0, len(y)) / sr

    # Find peak value and its index
    peak_value = np.max(np.abs(y))
    peak_index = np.argmax(np.abs(y))

    # Plot waveform
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, color='blue')
    plt.scatter(t[peak_index], y[peak_index], color='red', label=f'Peak Value: {peak_value:.2f}', zorder=5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio Waveform with Peak Value')
    plt.legend()
    plt.grid(True)
    output_path = 'static/waveform_with_peak.png'
    plt.savefig(output_path)
    plt.close()
    return output_path
