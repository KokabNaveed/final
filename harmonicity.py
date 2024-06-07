import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def get_harmonicity(file_path):
    y, sr = librosa.load(file_path)
    y_harm, y_perc = librosa.effects.hpss(y)
    # y_harm contains the musical (pitched) portion of the audio signal
    # y_perc contains the non musical (unpitched) portion of the audio signal
    harmonicity = librosa.feature.rms(y=y_harm)
    return harmonicity[0]

def plot_harmonicity(file_path):
    harmonicity = get_harmonicity(file_path)
    
    plt.figure(figsize=(10, 6))
    plt.plot(harmonicity)
    plt.title('Harmonicity')
    plt.xlabel('Frame')
    plt.ylabel('RMS Energy')
    plt.grid(True)
    output_path = 'static/harmonicity_plot.png'
    plt.savefig(output_path)
    plt.close()
    return output_path
