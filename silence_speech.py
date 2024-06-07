import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def get_silence_speech_ratio(file_path, silence_thresh=-40):
    y, sr = librosa.load(file_path)
    # y: audio time series, sr: sampling rate
    intervals = librosa.effects.split(y, top_db=-silence_thresh)
    # Split an audio signal into non-silent intervals
    total_duration = librosa.get_duration(y=y, sr=sr)
    speech_duration = np.sum(np.diff(intervals, axis=1)) / sr
    # Calculate speech duration by summing the difference between the start and end of each interval
    silence_duration = total_duration - speech_duration
    ratio = silence_duration / speech_duration
    return ratio, speech_duration, silence_duration

def plot_silence_speech_ratio_pie(file_path):
    ratio, speech_duration, silence_duration = get_silence_speech_ratio(file_path)

    # Calculate percentage of speech and silence
    total_duration = speech_duration + silence_duration
    speech_percentage = (speech_duration / total_duration) * 100
    silence_percentage = (silence_duration / total_duration) * 100

    # Plot pie chart
    labels = ['Speech', 'Silence']
    sizes = [speech_duration, silence_duration]
    colors = ['skyblue', 'lightgray']
    explode = (0.1, 0)  # explode the 1st slice
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Speech and Silence Duration')
    output_path = 'static/silence_speech_ratio_pie.png'
    plt.savefig(output_path)
    plt.close()
    return output_path
