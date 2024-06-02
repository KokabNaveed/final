import librosa
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import sqlite3
import os
from Bitrate import get_bitrate
from DR import calculate_decibels_with_sampling_rate, plot_waveform_with_sampling_rate
from loudness import get_loudness, plot_loudness
from peak_level import plot_waveform_with_peak
from silence_speech import get_silence_speech_ratio, plot_silence_speech_ratio_pie
from file_utils import calculate_file_size

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure the database and uploads directories exist
if not os.path.exists('database'):
    os.makedirs('database')
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''DROP TABLE IF EXISTS uploads''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        bitrate INTEGER NOT NULL,
                        loudness_plot_path TEXT NOT NULL,
                        waveform_plot_path TEXT NOT NULL,
                        silence_speech_ratio_plot_path TEXT NOT NULL,
                        plot_path_decibels TEXT NOT NULL,
                        plot_path_sr TEXT NOT NULL)''')
 
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        
        # Fetch user details from the database
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        # Check if user exists and passwords match
        if user and user[2] == password:  # Check password without hashing
            session['username'] = username
            conn.close()
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
            conn.close()
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        
        try:
            # Insert new user into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))  # Store password directly
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists")
            conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# Other routes remain the same

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        
        if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
            flash("Unsupported file format. Only .mp3 and .wav are allowed.")
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Calculate the bitrate using the get_bitrate function
        bitrate = get_bitrate(file_path)
        
        # Plot the waveform with sampling rate and save the plot
        plot_path_sr = plot_waveform_with_sampling_rate(file_path)

        # Plot the decibel range and save the plot
        plot_path_decibals = calculate_decibels_with_sampling_rate(file_path)

        
        # Plot the loudness and save the plot
        loudness_plot_path = plot_loudness(file_path)
        
        # Plot the waveform with peak and save the plot
        waveform_plot_path = plot_waveform_with_peak(file_path)

        # Plot the silence speech ratio pie chart and save the plot
        silence_speech_ratio_plot_path = plot_silence_speech_ratio_pie(file_path)

        # Calculate the file size
        file_size_mb = calculate_file_size(file_path)
        
        if file_size_mb is not None and bitrate is not None:
            conn = sqlite3.connect('database/users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO uploads (filename, bitrate, plot_path, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path) VALUES (?, ?, ?, ?, ?, ?)', 
                           (filename, bitrate, plot_path_sr,plot_path_decibals, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path,plot_path_decibals, plot_path_sr))
            conn.commit()
            conn.close()
            flash(f"File uploaded successfully with bitrate: {bitrate}")
        else:
            flash("Error calculating bitrate")
        
        # Pass the paths of the generated graph images to the template
        return render_template('upload.html', plot_path_sr_var=plot_path_sr,plot_path_decibals_var=plot_path_decibals,loudness_plot_path=loudness_plot_path, waveform_plot_path=waveform_plot_path, silence_speech_ratio_plot_path=silence_speech_ratio_plot_path, file_size_var=file_size_mb, bitrate_var=bitrate)
    
    return render_template('upload.html')

@app.route('/history')
def history():
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, bitrate, plot_path, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path FROM uploads')
    uploads = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', uploads=uploads)

if __name__ == '__main__':
    app.run(debug=True)
